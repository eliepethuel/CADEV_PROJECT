"""Sérialiseurs des échanges. Les compteurs viennent des annotations, jamais du client."""

from typing import Any

from rest_framework import serializers

from apps.accounts.models import User
from apps.catalog.models import Category, Tag, Technology
from apps.catalog.serializers import (
    CategoryRefSerializer,
    TagRefSerializer,
    TechnologyRefSerializer,
)
from apps.communities.models import Community
from common.sanitization import to_excerpt, to_plain_text

from .models import Answer, Comment, ContentStatus, Post

EXCERPT_LENGTH = 280
MAX_TAGS = 5
MAX_TECHNOLOGIES = 8
WRITABLE_TYPES = [
    (value, label) for value, label in Post.Type.choices if value != Post.Type.PROJECT_UPDATE
]


class AuthorSerializer(serializers.Serializer):
    """Identité publique d'un auteur : jamais d'e-mail ni de champ privé."""

    username = serializers.CharField()
    display_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_display_name(self, user: User) -> str:
        profile = getattr(user, "profile", None)
        return profile.display_name if profile else user.username

    def get_avatar(self, user: User) -> str | None:
        profile = getattr(user, "profile", None)
        if not profile or not profile.avatar:
            return None
        request = self.context.get("request")
        url = profile.avatar.url
        return request.build_absolute_uri(url) if request else url


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategoryRefSerializer(read_only=True)
    tags = TagRefSerializer(many=True, read_only=True)
    technologies = TechnologyRefSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    vote_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    answer_count = serializers.IntegerField(read_only=True)
    has_accepted_answer = serializers.BooleanField(read_only=True)
    has_voted = serializers.BooleanField(read_only=True)
    has_bookmarked = serializers.BooleanField(read_only=True)
    community = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "type",
            "title",
            "excerpt",
            "author",
            "category",
            "tags",
            "technologies",
            "status",
            "vote_count",
            "comment_count",
            "answer_count",
            "has_accepted_answer",
            "has_voted",
            "has_bookmarked",
            "community",
            "published_at",
            "last_activity_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_excerpt(self, post: Post) -> str:
        return to_excerpt(post.content, EXCERPT_LENGTH)


class PostDetailSerializer(PostListSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = [*PostListSerializer.Meta.fields, "content", "environment", "can_edit"]
        read_only_fields = fields

    def get_can_edit(self, post: Post) -> bool:
        request = self.context.get("request")
        return bool(
            request
            and request.user.is_authenticated
            and post.author_id == request.user.pk
            and post.status in (ContentStatus.DRAFT, ContentStatus.PUBLISHED)
        )


class PostWriteSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=WRITABLE_TYPES, default=Post.Type.DISCUSSION)
    status = serializers.ChoiceField(
        choices=[ContentStatus.DRAFT, ContentStatus.PUBLISHED],
        default=ContentStatus.PUBLISHED,
        help_text="DRAFT pour un brouillon ; un brouillon ne peut qu'être publié ensuite.",
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.filter(is_active=True)
    )
    tags = serializers.SlugRelatedField(
        slug_field="slug", many=True, required=False, queryset=Tag.objects.filter(is_active=True)
    )
    technologies = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        required=False,
        queryset=Technology.objects.filter(is_active=True),
    )
    content = serializers.CharField(
        required=False, allow_blank=True, max_length=Post.CONTENT_MAX_LENGTH, trim_whitespace=False
    )
    environment = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    community = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Community.objects.filter(hidden_by_moderation=False),
        required=False,
        allow_null=True,
        help_text="Slug d'une communauté dont l'auteur est membre (P2).",
    )

    class Meta:
        model = Post
        fields = [
            "type",
            "title",
            "content",
            "environment",
            "category",
            "tags",
            "technologies",
            "status",
            "community",
        ]

    def validate_title(self, value: str) -> str:
        value = to_plain_text(value)
        if len(value) < Post.TITLE_MIN_LENGTH:
            raise serializers.ValidationError(
                f"Le titre doit contenir au moins {Post.TITLE_MIN_LENGTH} caractères."
            )
        return value

    def validate_tags(self, value: list[Tag]) -> list[Tag]:
        if len(value) > MAX_TAGS:
            raise serializers.ValidationError(f"{MAX_TAGS} tags au maximum.")
        return value

    def validate_technologies(self, value: list[Technology]) -> list[Technology]:
        if len(value) > MAX_TECHNOLOGIES:
            raise serializers.ValidationError(f"{MAX_TECHNOLOGIES} technologies au maximum.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    is_removed = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent",
            "author",
            "content",
            "is_removed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def _removed(self, comment: Comment) -> bool:
        return comment.status != ContentStatus.PUBLISHED

    def get_is_removed(self, comment: Comment) -> bool:
        return self._removed(comment)

    def get_author(self, comment: Comment) -> dict[str, Any] | None:
        if self._removed(comment):
            return None
        return AuthorSerializer(comment.author, context=self.context).data

    def get_content(self, comment: Comment) -> str:
        return "" if self._removed(comment) else comment.content


class CommentWriteSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=Comment.MAX_LENGTH)
    parent = serializers.UUIDField(required=False, allow_null=True)


class AnswerSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    vote_count = serializers.IntegerField(read_only=True)
    has_voted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "author",
            "content",
            "is_accepted",
            "accepted_at",
            "vote_count",
            "has_voted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class AnswerWriteSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=Answer.MAX_LENGTH)


class VoteInputSerializer(serializers.Serializer):
    active = serializers.BooleanField(
        required=False,
        allow_null=True,
        default=None,
        help_text="true : voter, false : retirer. Absent : bascule l'état actuel.",
    )


class VoteResultSerializer(serializers.Serializer):
    voted = serializers.BooleanField()
    vote_count = serializers.IntegerField()


class BookmarkResultSerializer(serializers.Serializer):
    bookmarked = serializers.BooleanField()
