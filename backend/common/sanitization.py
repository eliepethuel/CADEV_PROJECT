"""Assainissement des contenus riches saisis par les membres."""

import html
import re

import nh3

ALLOWED_TAGS: set[str] = {
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "h2",
    "h3",
    "h4",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "ul",
}
ALLOWED_ATTRIBUTES: dict[str, set[str]] = {"a": {"href", "title"}, "code": {"class"}}
ALLOWED_URL_SCHEMES: set[str] = {"http", "https", "mailto"}
# Fin de bloc ou saut de ligne : à remplacer par une espace avant de retirer les balises.
_BLOCK_BOUNDARY = re.compile(
    r"</(?:p|h[1-6]|li|ul|ol|pre|blockquote|div|tr)\s*>|<(?:br|hr)\s*/?>", re.IGNORECASE
)


def sanitize_rich_text(value: str | None) -> str:
    """Ne conserve qu'une liste blanche de balises et de schémas d'URL."""
    if not value:
        return ""
    return nh3.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        link_rel="noopener noreferrer nofollow",
    ).strip()


def has_visible_text(value: str | None) -> bool:
    """Vrai si le contenu garde du texte une fois toutes les balises retirées."""
    if not value:
        return False
    return bool(nh3.clean(value, tags=set()).strip())


def to_plain_text(value: str | None) -> str:
    """Retire toute balise HTML d'un champ texte simple (biographie, message court)."""
    if not value:
        return ""
    return html.unescape(nh3.clean(value, tags=set())).strip()


def to_excerpt(value: str | None, length: int) -> str:
    """Extrait en texte brut d'un contenu riche, sans coller les blocs entre eux."""
    if not value:
        return ""
    text = " ".join(to_plain_text(_BLOCK_BOUNDARY.sub(" ", value)).split())
    return text if len(text) <= length else f"{text[: length - 1].rstrip()}…"
