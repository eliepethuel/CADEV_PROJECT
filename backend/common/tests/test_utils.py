import io
import json
import logging

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from PIL import Image
from rest_framework import exceptions

from common.exceptions import BusinessRuleViolation, InvalidTransition, api_exception_handler
from common.logging import JSONFormatter
from common.sanitization import has_visible_text, sanitize_rich_text, to_excerpt
from common.transitions import can_transition, ensure_transition
from common.validators import validate_http_url, validate_image_upload

TABLE = {"DRAFT": {"PUBLISHED"}, "PUBLISHED": {"HIDDEN"}}


def make_image(name="avatar.png", fmt="PNG", size=(32, 32)) -> SimpleUploadedFile:
    buffer = io.BytesIO()
    Image.new("RGB", size, "green").save(buffer, fmt)
    return SimpleUploadedFile(name, buffer.getvalue())


class TestTransitions:
    def test_allowed_transition_passes(self):
        assert can_transition(TABLE, "DRAFT", "PUBLISHED")
        ensure_transition(TABLE, "DRAFT", "PUBLISHED")

    def test_forbidden_transition_raises(self):
        with pytest.raises(InvalidTransition):
            ensure_transition(TABLE, "HIDDEN", "DRAFT")


class TestSanitization:
    def test_script_and_event_handlers_are_removed(self):
        cleaned = sanitize_rich_text('<p onclick="x()">Salut</p><script>alert(1)</script>')

        assert cleaned == "<p>Salut</p>"

    def test_javascript_links_are_neutralised(self):
        cleaned = sanitize_rich_text('<a href="javascript:alert(1)">clic</a>')

        assert "javascript" not in cleaned

    def test_safe_links_get_rel_attribute(self):
        cleaned = sanitize_rich_text('<a href="https://example.org">doc</a>')

        assert 'href="https://example.org"' in cleaned
        assert "noopener" in cleaned

    def test_empty_values(self):
        assert sanitize_rich_text(None) == ""
        assert not has_visible_text("<p> </p>")
        assert has_visible_text("<p>ok</p>")


class TestExcerpt:
    def test_block_elements_are_separated_by_a_space(self):
        content = (
            "<h2>Objectif</h2><p>Un déploiement.</p><ul><li>Dockerfile</li><li>Compose</li></ul>"
        )

        assert to_excerpt(content, 200) == "Objectif Un déploiement. Dockerfile Compose"

    def test_inline_elements_stay_attached_to_their_punctuation(self):
        assert to_excerpt("<p>Utilisez <code>Count</code>, puis testez.</p>", 200) == (
            "Utilisez Count, puis testez."
        )

    def test_long_text_is_truncated_with_an_ellipsis(self):
        excerpt = to_excerpt("<p>" + "mot " * 100 + "</p>", 20)

        assert len(excerpt) <= 20
        assert excerpt.endswith("…")

    def test_empty_content(self):
        assert to_excerpt(None, 50) == ""


class TestUrlValidator:
    @pytest.mark.parametrize("url", ["https://github.com/afridev", "http://example.org/a?b=1"])
    def test_http_urls_are_accepted(self, url):
        validate_http_url(url)

    @pytest.mark.parametrize(
        "url", ["javascript:alert(1)", "ftp://example.org", "data:text/html,x", "example.org"]
    )
    def test_other_schemes_are_rejected(self, url):
        with pytest.raises(ValidationError):
            validate_http_url(url)


class TestImageValidator:
    def test_valid_png_is_accepted(self):
        validate_image_upload(make_image())

    def test_non_image_content_is_rejected(self):
        with pytest.raises(ValidationError) as error:
            validate_image_upload(SimpleUploadedFile("avatar.png", b"<?php echo 1; ?>"))
        assert error.value.code == "invalid_image"

    def test_extension_must_match_content(self):
        with pytest.raises(ValidationError) as error:
            validate_image_upload(make_image(name="avatar.jpg", fmt="PNG"))
        assert error.value.code == "invalid_extension"

    def test_unsupported_format_is_rejected(self):
        with pytest.raises(ValidationError) as error:
            validate_image_upload(make_image(name="avatar.gif", fmt="GIF"))
        assert error.value.code == "invalid_image_type"

    def test_oversized_file_is_rejected(self, settings):
        settings.MAX_IMAGE_UPLOAD_BYTES = 10
        with pytest.raises(ValidationError) as error:
            validate_image_upload(make_image())
        assert error.value.code == "file_too_large"

    def test_huge_dimensions_are_rejected(self):
        with pytest.raises(ValidationError) as error:
            validate_image_upload(make_image(size=(5000, 10)))
        assert error.value.code == "image_too_large"


class TestExceptionHandler:
    def test_validation_error_format(self):
        response = api_exception_handler(exceptions.ValidationError({"title": ["Requis."]}), {})

        assert response.status_code == 400
        assert response.data["code"] == "validation_error"
        assert response.data["errors"] == {"title": ["Requis."]}

    def test_list_validation_error_is_wrapped(self):
        response = api_exception_handler(exceptions.ValidationError(["Invalide."]), {})

        assert response.data["errors"] == {"non_field_errors": ["Invalide."]}

    def test_business_rule_violation_is_a_conflict(self):
        response = api_exception_handler(BusinessRuleViolation("Interdit.", code="nope"), {})

        assert response.status_code == 409
        assert response.data == {"detail": "Interdit.", "code": "nope", "errors": {}}

    def test_django_exceptions_are_translated(self):
        assert api_exception_handler(Http404(), {}).data["code"] == "not_found"
        assert api_exception_handler(PermissionDenied(), {}).data["code"] == "permission_denied"
        assert api_exception_handler(ValidationError("x"), {}).status_code == 400
        assert api_exception_handler(ValidationError({"a": ["x"]}), {}).data["errors"] == {
            "a": ["x"]
        }

    def test_unknown_exception_is_not_swallowed(self):
        assert api_exception_handler(RuntimeError("boom"), {}) is None


def test_json_formatter_masks_sensitive_context():
    record = logging.LogRecord("app", logging.INFO, __file__, 1, "connexion", None, None)
    record.context = {"password": "secret", "user": "awa"}

    payload = json.loads(JSONFormatter().format(record))

    assert payload["message"] == "connexion"
    assert payload["context"] == {"password": "[masqué]", "user": "awa"}
