"""Réglages communs à tous les environnements."""

from datetime import timedelta
from pathlib import Path

import environ

from .admin_theme import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS, LOGIN_REDIRECT_URL  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(ROOT_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

DJANGO_APPS = [
    # Thème de l'administration : doit précéder django.contrib.admin.
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]

LOCAL_APPS = [
    "common",
    "apps.accounts",
    "apps.catalog",
    "apps.profiles",
    "apps.notifications",
    "apps.community",
    "apps.projects",
    "apps.moderation",
    "apps.social",
    "apps.reputation",
    "apps.opportunities",
    "apps.mentorship",
    "apps.communities",
    "apps.events",
    "apps.messaging",
    "apps.search",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Base de données -----------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://afridev:afridev@localhost:5434/afridev",
    ),
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DATABASE_CONN_MAX_AGE", default=60)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

# Mots de passe -------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
PASSWORD_RESET_TIMEOUT = env.int("PASSWORD_RESET_TIMEOUT", default=60 * 60)

# Internationalisation ------------------------------------------------------
LANGUAGE_CODE = "fr"
LANGUAGES = [("fr", "Français"), ("en", "English")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Fichiers statiques et médias ----------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = Path(env("DJANGO_MEDIA_ROOT", default=str(ROOT_DIR / "media")))
SERVE_MEDIA = env.bool("DJANGO_SERVE_MEDIA", default=False)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "common.storage.StaticStorage"},
}
MAX_IMAGE_UPLOAD_BYTES = env.int("MAX_IMAGE_UPLOAD_BYTES", default=2 * 1024 * 1024)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# CORS / CSRF ---------------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# E-mail --------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="AfriDev Community <no-reply@afridev.local>")
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:3000")
# Le lien « Site » de l'administration ouvre le frontend.
JAZZMIN_SETTINGS["topmenu_links"][0]["url"] = FRONTEND_URL

# Django REST Framework -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "common.pagination.StandardPagination",
    "PAGE_SIZE": env.int("API_PAGE_SIZE", default=20),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "common.exceptions.api_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "common.throttling.ScopedWriteThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": env("THROTTLE_ANON", default="120/min"),
        "user": env("THROTTLE_USER", default="300/min"),
        "login": env("THROTTLE_LOGIN", default="10/min"),
        "token_refresh": env("THROTTLE_TOKEN_REFRESH", default="60/min"),
        "register": env("THROTTLE_REGISTER", default="10/hour"),
        "password_reset": env("THROTTLE_PASSWORD_RESET", default="5/hour"),
        "content_create": env("THROTTLE_CONTENT_CREATE", default="30/hour"),
        "comment_create": env("THROTTLE_COMMENT_CREATE", default="60/hour"),
        "report_create": env("THROTTLE_REPORT_CREATE", default="20/hour"),
        "join_request": env("THROTTLE_JOIN_REQUEST", default="20/hour"),
        "messaging": env("THROTTLE_MESSAGING", default="60/hour"),
        "search": env("THROTTLE_SEARCH", default="60/min"),
    },
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
API_MAX_PAGE_SIZE = env.int("API_MAX_PAGE_SIZE", default=100)

# JWT -----------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_MINUTES", default=15)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_DAYS", default=7)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
AUTH_COOKIE = {
    "NAME": env("AUTH_COOKIE_NAME", default="afridev_refresh"),
    "SECURE": env.bool("AUTH_COOKIE_SECURE", default=True),
    "SAMESITE": env("AUTH_COOKIE_SAMESITE", default="Lax"),
    "DOMAIN": env("AUTH_COOKIE_DOMAIN", default=None),
    "PATH": "/api/v1/auth/",
}

# OpenAPI -------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "AfriDev Community API",
    "DESCRIPTION": (
        "API REST de la plateforme communautaire AfriDev Community : échanges techniques, "
        "profils développeurs, projets collaboratifs et modération."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "ENUM_NAME_OVERRIDES": {
        "ContentStatusEnum": "apps.community.models.ContentStatus",
        "PostTypeEnum": "apps.community.models.Post.Type",
        "ExperienceLevelEnum": "apps.profiles.models.ExperienceLevel",
        "ProjectStatusEnum": "apps.projects.models.Project.Status",
        "MemberStatusEnum": "apps.projects.models.ProjectMember.Status",
        "JoinRequestStatusEnum": "apps.projects.models.JoinRequest.Status",
        "TaskStatusEnum": "apps.projects.models.ProjectTask.Status",
        "ReportStatusEnum": "apps.moderation.models.Report.Status",
        "NotificationTypeEnum": "apps.notifications.models.Notification.Type",
        "ModerationActionTypeEnum": "apps.moderation.models.ModerationAction.ActionType",
        "ReportTargetTypeEnum": "apps.moderation.models.TargetType",
        "FollowTargetTypeEnum": "apps.social.models.Follow.TargetType",
        "GlobalRoleEnum": "apps.accounts.models.User.Role",
        "OpportunityTypeEnum": "apps.opportunities.models.Opportunity.Type",
        "CollaborationModeEnum": "apps.projects.models.Project.CollaborationMode",
        "CommunityRoleEnum": "apps.communities.models.CommunityMembership.Role",
        "CommunityKindEnum": "apps.communities.models.Community.Kind",
        "EventKindEnum": "apps.events.models.Event.Kind",
        "ProjectRoleEnum": "apps.projects.models.ProjectMember.Role",
        "AssignableProjectRoleEnum": "apps.projects.models.ASSIGNABLE_ROLE_CHOICES",
    },
}

# Journalisation ------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {asctime} {name} {message}", "style": "{"},
        "json": {"()": "common.logging.JSONFormatter"},
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": env("DJANGO_LOG_LEVEL", default="INFO")},
}
