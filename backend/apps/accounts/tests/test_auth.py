import pytest
from django.conf import settings
from django.core import mail

from apps.accounts.models import User
from apps.accounts.tests.factories import DEFAULT_PASSWORD, UserFactory
from common.throttling import ScopedWriteThrottle

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
REFRESH_URL = "/api/v1/auth/token/refresh/"
LOGOUT_URL = "/api/v1/auth/logout/"
ME_URL = "/api/v1/auth/me/"
COOKIE = settings.AUTH_COOKIE["NAME"]

VALID_PAYLOAD = {
    "username": "fatou_dev",
    "email": "Fatou.Dev@Example.org",
    "password": "Harmattan-Clair-2026",
}


def login(client, identifier="awa", password=DEFAULT_PASSWORD):
    return client.post(LOGIN_URL, {"identifier": identifier, "password": password})


class TestRegister:
    def test_visitor_creates_an_account(self, api_client, django_capture_on_commit_callbacks):
        with django_capture_on_commit_callbacks(execute=True):
            response = api_client.post(REGISTER_URL, VALID_PAYLOAD)

        assert response.status_code == 201
        body = response.json()
        assert body["user"]["username"] == "fatou_dev"
        assert body["user"]["email"] == "fatou.dev@example.org"
        assert body["user"]["role"] == "MEMBER"
        assert "password" not in body["user"]
        assert "refresh" not in body
        created = User.objects.get(username="fatou_dev")
        assert created.check_password(VALID_PAYLOAD["password"])
        assert not created.password.startswith(VALID_PAYLOAD["password"])
        assert len(mail.outbox) == 1
        assert "verifier-email" in mail.outbox[0].body

    def test_registration_opens_a_session(self, api_client):
        response = api_client.post(REGISTER_URL, VALID_PAYLOAD)

        cookie = response.cookies[COOKIE]
        assert cookie["httponly"]
        assert cookie["path"] == "/api/v1/auth/"
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")
        assert api_client.get(ME_URL).status_code == 200

    def test_privileged_fields_are_ignored(self, api_client):
        payload = {
            **VALID_PAYLOAD,
            "role": "ADMIN",
            "is_staff": True,
            "is_superuser": True,
            "email_verified": True,
        }

        api_client.post(REGISTER_URL, payload)

        created = User.objects.get(username="fatou_dev")
        assert created.role == User.Role.MEMBER
        assert not created.is_staff
        assert not created.is_superuser
        assert not created.email_verified

    def test_duplicate_email_is_refused_case_insensitively(self, api_client, user):
        payload = {**VALID_PAYLOAD, "email": user.email.upper()}

        response = api_client.post(REGISTER_URL, payload)

        assert response.status_code == 400
        body = response.json()
        assert body["code"] == "validation_error"
        assert "déjà" in body["errors"]["email"][0]

    def test_duplicate_username_is_refused_case_insensitively(self, api_client, user):
        response = api_client.post(REGISTER_URL, {**VALID_PAYLOAD, "username": "AWA"})

        assert response.status_code == 400
        assert "username" in response.json()["errors"]

    @pytest.mark.parametrize("username", ["ab", "avec espace", "9lives", "émilie", "a" * 31, "me"])
    def test_invalid_usernames_are_refused(self, api_client, username):
        response = api_client.post(REGISTER_URL, {**VALID_PAYLOAD, "username": username})

        assert response.status_code == 400
        assert "username" in response.json()["errors"]

    @pytest.mark.parametrize("password", ["court", "1234567890", "motdepasse", "fatou_dev"])
    def test_weak_passwords_are_refused(self, api_client, password):
        response = api_client.post(REGISTER_URL, {**VALID_PAYLOAD, "password": password})

        assert response.status_code == 400
        assert "password" in response.json()["errors"]
        assert not User.objects.filter(username="fatou_dev").exists()

    def test_missing_fields_are_reported(self, api_client):
        response = api_client.post(REGISTER_URL, {})

        assert set(response.json()["errors"]) == {"username", "email", "password"}


class TestLogin:
    @pytest.mark.parametrize("identifier", ["awa", "AWA", "awa@example.org", "Awa@Example.org"])
    def test_login_with_username_or_email(self, api_client, user, identifier):
        response = login(api_client, identifier)

        assert response.status_code == 200
        assert response.json()["user"]["id"] == str(user.id)
        assert COOKIE in response.cookies

    def test_wrong_password_is_rejected(self, api_client, user):
        response = login(api_client, password="mauvais-mot-de-passe")

        assert response.status_code == 401
        assert response.json()["code"] == "invalid_credentials"
        assert COOKIE not in response.cookies

    def test_unknown_account_gets_the_same_error(self, api_client):
        response = login(api_client, "inconnu")

        assert response.status_code == 401
        assert response.json()["code"] == "invalid_credentials"

    def test_disabled_account_cannot_login(self, api_client):
        UserFactory(username="banni", is_active=False)

        assert login(api_client, "banni").status_code == 401

    def test_login_is_rate_limited(self, api_client, user, monkeypatch):
        monkeypatch.setitem(ScopedWriteThrottle.THROTTLE_RATES, "login", "2/min")

        statuses = [login(api_client, password="faux").status_code for _ in range(3)]

        assert statuses == [401, 401, 429]


class TestProtectedRoutes:
    def test_anonymous_cannot_read_account(self, api_client):
        response = api_client.get(ME_URL)

        assert response.status_code == 401
        assert response.json()["code"] == "not_authenticated"

    def test_garbage_token_is_rejected(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer pas-un-jeton")

        assert api_client.get(ME_URL).status_code == 401

    def test_disabled_account_token_is_rejected(self, api_client, user):
        access = login(api_client).json()["access"]
        User.objects.filter(pk=user.pk).update(is_active=False)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        assert api_client.get(ME_URL).status_code == 401


class TestRefresh:
    def test_refresh_rotates_the_cookie(self, api_client, user):
        first_cookie = login(api_client).cookies[COOKIE].value

        response = api_client.post(REFRESH_URL)

        assert response.status_code == 200
        assert set(response.json()) == {"access"}
        assert response.cookies[COOKIE].value != first_cookie

    def test_rotated_token_cannot_be_replayed(self, api_client, user):
        old_cookie = login(api_client).cookies[COOKIE].value
        api_client.post(REFRESH_URL)
        api_client.cookies[COOKIE] = old_cookie

        response = api_client.post(REFRESH_URL)

        assert response.status_code == 401
        assert response.json()["code"] == "refresh_token_invalid"

    def test_refresh_does_not_consume_the_login_limit(self, api_client, user, monkeypatch):
        monkeypatch.setitem(ScopedWriteThrottle.THROTTLE_RATES, "login", "2/min")

        statuses = [api_client.post(REFRESH_URL).status_code for _ in range(3)]

        assert statuses == [401, 401, 401]
        assert login(api_client).status_code == 200

    def test_refresh_has_its_own_rate_limit(self, api_client, monkeypatch):
        monkeypatch.setitem(ScopedWriteThrottle.THROTTLE_RATES, "token_refresh", "2/min")

        statuses = [api_client.post(REFRESH_URL).status_code for _ in range(3)]

        assert statuses == [401, 401, 429]

    def test_refresh_without_cookie(self, api_client):
        response = api_client.post(REFRESH_URL)

        assert response.status_code == 401
        assert response.json()["code"] == "refresh_token_missing"

    def test_refresh_from_untrusted_origin_is_blocked(self, api_client, user):
        login(api_client)

        response = api_client.post(REFRESH_URL, HTTP_ORIGIN="https://evil.example")

        assert response.status_code == 403
        assert response.json()["code"] == "untrusted_origin"

    def test_refresh_from_allowed_origin(self, api_client, user):
        login(api_client)

        response = api_client.post(REFRESH_URL, HTTP_ORIGIN="http://localhost:3000")

        assert response.status_code == 200

    def test_disabled_account_cannot_refresh(self, api_client, user):
        login(api_client)
        User.objects.filter(pk=user.pk).update(is_active=False)

        response = api_client.post(REFRESH_URL)

        assert response.status_code == 401
        assert response.json()["code"] == "account_disabled"


class TestLogout:
    def test_logout_revokes_the_session(self, api_client, user):
        cookie = login(api_client).cookies[COOKIE].value

        response = api_client.post(LOGOUT_URL)

        assert response.status_code == 204
        assert response.cookies[COOKIE].value == ""
        api_client.cookies[COOKIE] = cookie
        assert api_client.post(REFRESH_URL).status_code == 401

    def test_logout_is_idempotent(self, api_client):
        assert api_client.post(LOGOUT_URL).status_code == 204
        api_client.cookies[COOKIE] = "jeton-invalide"
        assert api_client.post(LOGOUT_URL).status_code == 204

    def test_logout_from_untrusted_origin_is_blocked(self, api_client, user):
        login(api_client)

        response = api_client.post(LOGOUT_URL, HTTP_ORIGIN="https://evil.example")

        assert response.status_code == 403


class TestSuspension:
    def test_suspended_account_is_told_only_with_right_password(self, api_client):
        from datetime import timedelta

        from django.utils import timezone

        UserFactory(
            username="suspendu",
            is_active=False,
            suspended_until=timezone.now() + timedelta(days=3),
        )

        right = login(api_client, "suspendu")
        wrong = login(api_client, "suspendu", password="mauvais-mot-de-passe")

        assert right.status_code == 403
        assert right.json()["code"] == "account_suspended"
        assert wrong.status_code == 401
        assert wrong.json()["code"] == "invalid_credentials"

    def test_expired_suspension_is_lifted_at_login(self, api_client):
        from datetime import timedelta

        from django.utils import timezone

        member = UserFactory(
            username="revenu", is_active=False, suspended_until=timezone.now() - timedelta(hours=1)
        )

        assert login(api_client, "revenu").status_code == 200
        member.refresh_from_db()
        assert member.is_active and member.suspended_until is None

    def test_banned_account_stays_disabled(self, api_client):
        from datetime import timedelta

        from django.utils import timezone

        UserFactory(
            username="banni2",
            is_active=False,
            banned_at=timezone.now(),
            suspended_until=timezone.now() - timedelta(days=1),
        )

        assert login(api_client, "banni2").status_code == 401
