"""Registre des cibles signalables : chargement, auteur, aperçu et actions possibles.

Chaque module enregistre ses cibles ; la modération reste ainsi découplée des
modèles qu'elle traite. Les modules P2 (opportunités, messages, événements,
communautés) s'y ajoutent via ``register``.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from django.db.models import Model

from .models import ModerationAction, TargetType

Action = ModerationAction.ActionType
ACCOUNT_ACTIONS = {Action.WARNING, Action.SUSPEND, Action.UNSUSPEND, Action.BAN, Action.UNBAN}


@dataclass(frozen=True)
class TargetSpec:
    loader: Callable[[Any], Model | None]
    author: Callable[[Model], Any]
    preview: Callable[[Model], dict[str, Any]]
    visible_to: Callable[[Model, Any], bool]
    actions: set[str] = field(default_factory=set)
    # Masquage / restauration propre à la cible : (objet, masquer ?) -> (avant, après).
    hide: Callable[[Model, bool], tuple[str, str]] | None = None


REGISTRY: dict[str, TargetSpec] = {}


def register(target_type: str, spec: TargetSpec) -> None:
    REGISTRY[target_type] = spec


def get_spec(target_type: str) -> TargetSpec | None:
    _ensure_defaults()
    return REGISTRY.get(target_type)


def _excerpt(text: str, length: int = 200) -> str:
    from common.sanitization import to_excerpt

    return to_excerpt(text, length)


def flag_hider(flag: str = "hidden_by_moderation") -> Callable[[Model, bool], tuple[str, str]]:
    """Masquage par drapeau booléen (projets, opportunités, événements, communautés…)."""

    def hide(obj: Model, wanted: bool) -> tuple[str, str]:
        from common.exceptions import BusinessRuleViolation

        current = getattr(obj, flag)
        if current == wanted:
            raise BusinessRuleViolation(
                "La cible est déjà dans cet état.", code="invalid_transition"
            )
        setattr(obj, flag, wanted)
        obj.save(update_fields=[flag, "updated_at"])
        return ("HIDDEN" if current else "VISIBLE"), ("HIDDEN" if wanted else "VISIBLE")

    return hide


def account_state(account: Any) -> str:
    """État lisible d'un compte pour la file de modération."""
    if account.is_banned:
        return "BANNED"
    if account.is_suspended:
        return "SUSPENDED"
    return "ACTIVE" if account.is_active else "INACTIVE"


_defaults_loaded = False


def _ensure_defaults() -> None:
    """Enregistre les cibles P0 au premier usage (évite les imports circulaires)."""
    global _defaults_loaded
    if _defaults_loaded:
        return
    _defaults_loaded = True

    from apps.accounts.models import User
    from apps.community.models import Answer, Comment, ContentStatus, Post
    from apps.projects import policies as project_policies
    from apps.projects.models import Project

    content_actions = {Action.WARNING, Action.HIDE, Action.RESTORE, Action.DELETE} | ACCOUNT_ACTIONS

    def load(model: Any) -> Callable[[Any], Model | None]:
        manager = getattr(model, "all_objects", model.objects)
        return lambda pk: manager.filter(pk=pk).first()

    def published(obj: Model, user: Any) -> bool:
        return obj.status == ContentStatus.PUBLISHED

    register(
        TargetType.POST,
        TargetSpec(
            loader=load(Post),
            author=lambda post: post.author,
            preview=lambda post: {
                "title": post.title,
                "excerpt": _excerpt(post.content),
                "status": post.status,
                "url": f"/publications/{post.pk}",
            },
            visible_to=published,
            actions=content_actions,
        ),
    )
    register(
        TargetType.COMMENT,
        TargetSpec(
            loader=load(Comment),
            author=lambda comment: comment.author,
            preview=lambda comment: {
                "title": f"Commentaire sur « {comment.post.title} »",
                "excerpt": _excerpt(comment.content),
                "status": comment.status,
                "url": f"/publications/{comment.post_id}",
            },
            visible_to=published,
            actions=content_actions,
        ),
    )
    register(
        TargetType.ANSWER,
        TargetSpec(
            loader=load(Answer),
            author=lambda answer: answer.author,
            preview=lambda answer: {
                "title": f"Réponse à « {answer.question.title} »",
                "excerpt": _excerpt(answer.content),
                "status": answer.status,
                "url": f"/publications/{answer.question_id}",
            },
            visible_to=published,
            actions=content_actions,
        ),
    )
    register(
        TargetType.PROFILE,
        TargetSpec(
            loader=lambda pk: User.objects.filter(pk=pk).select_related("profile").first(),
            author=lambda account: account,
            preview=lambda account: {
                "title": account.username,
                "excerpt": _excerpt(getattr(getattr(account, "profile", None), "bio", "")),
                "status": account_state(account),
                "url": f"/membres/{account.username}",
            },
            visible_to=lambda account, user: account.is_active,
            actions=ACCOUNT_ACTIONS,
        ),
    )
    register(
        TargetType.PROJECT,
        TargetSpec(
            loader=load(Project),
            author=lambda project: project.owner,
            preview=lambda project: {
                "title": project.name,
                "excerpt": _excerpt(project.short_description),
                "status": "HIDDEN" if project.hidden_by_moderation else project.status,
                "url": f"/projets/{project.slug}",
            },
            visible_to=lambda project, user: project_policies.can_view(project, user),
            actions={Action.WARNING, Action.HIDE, Action.RESTORE} | ACCOUNT_ACTIONS,
            hide=flag_hider(),
        ),
    )
