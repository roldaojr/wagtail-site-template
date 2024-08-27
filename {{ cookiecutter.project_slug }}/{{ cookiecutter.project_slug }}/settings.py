"""
Django settings for '{{ cookiecutter.project_name }}' project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from email.utils import getaddresses
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

import environ
import sentry_sdk
import logging
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from ._version import __version__


BASE_DIR = Path(environ.Path(__file__) - 2)
PROJECT_DIR = Path(environ.Path(__file__) - 1)

# read enviroment variables
env = environ.FileAwareEnv()

# read .env from file if exists
DOT_ENV = BASE_DIR / ".env"
if DOT_ENV.is_file():
    env.read_env()

# read .env from enviroment variable
ENV_FILE = env("ENV_FILE", default=None)
if ENV_FILE:
    env.read_env(StringIO(ENV_FILE))

# environment settings
ENVIRONMENT = env.str("ENVIRONMENT", default="develop")
DEBUG = env.bool("DEBUG", default=True)

# application host name
VIRTUAL_HOST = env.str("VIRTUAL_HOST", default="localhost")

# secuirty settings
SECRET_KEY = env.str("SECRET_KEY", default="dummy")
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1", VIRTUAL_HOST])
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = "SAMEORIGIN"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=[f"https://{VIRTUAL_HOST}"]
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    # This project
    "website",
    # Wagtail CRX (CodeRed Extensions)
    "coderedcms",
    "django_bootstrap5",
    "modelcluster",
    "taggit",
    "wagtailcache",
    "wagtailseo",
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail",
    "wagtail.contrib.settings",
    "wagtail.contrib.table_block",
    "wagtail.admin",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # aditional apps
    "storages",
    "dbbackup",
    "sass_processor",
]

MIDDLEWARE = [
    # Save pages to cache. Must be FIRST.
    "wagtailcache.cache.UpdateCacheMiddleware",
    # Common functionality
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Security
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # CMS functionality
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # Fetch from cache. Must be LAST.
    "wagtailcache.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASE_URL = env("DATABASE_URL", default="sqlite:///db.sqlite3")
DATABASES = {"default": env.db(default="sqlite:///db.sqlite3")}

# cache config
CACHES = {"default": env.cache(default="locmemcache://")}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "pt-br"
LANGUAGES = [("pt-br", _("Potuguês Brasil"))]
TIME_ZONE = env("TIME_ZONE", default="America/Recife")
USE_I18N = True
USE_TZ = True

# file storage config
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

STATIC_ROOT = env.str("STATIC_ROOT", default=str(BASE_DIR / "static"))
STATIC_URL = env("STATIC_URL", default="/static/")

# {% if cookiecutter.whitenoise_static %}
# Whitenoiise
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
if not DEBUG:
    STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# {% endif %}

# enable SASS preprocessor
COMPRESS_OFFLINE = True
SASS_PROCESSOR_AUTO_INCLUDE = True
SASS_OUTPUT_STYLE = "compact"

# Media files
MEDIA_ROOT = env.str("MEDIA_ROOT", default=str(BASE_DIR / "media"))
MEDIA_URL = env.str("MEDIA_URL", default="/media/")

DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024**2  # max upload data 20 MB
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# Email config
ADMINS = getaddresses([env("ADMINS", default="")])
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=None)
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
vars().update(env.email_url("EMAIL_URL", default="consolemail://"))

# Login
LOGIN_URL = "wagtailadmin_login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"

# Wagtail settings
WAGTAIL_SITE_NAME = "{{ cookiecutter.project_name }}"
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]
WAGTAIL_I18N_ENABLED = False
WAGTAILADMIN_COMMENTS_ENABLED = False
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 8 * 1024**2  # 8 MB
WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", f"https://{VIRTUAL_HOST}")

# Tags
TAGGIT_CASE_INSENSITIVE = True

# Sets default for primary key IDs
# See https://docs.djangoproject.com/en/4.1/ref/models/fields/#bigautofield
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# logging - Enable log to console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Sentry error reporter
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:  # sentry is configured
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

    SENTRY_LOG_LEVEL = env.int("SENTRY_LOG_LEVEL", logging.INFO)
    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, DjangoIntegration(), RedisIntegration(), CeleryIntegration()],
        environment=ENVIRONMENT,
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
    # ignore DisallowedHost
    ignore_logger("django.security.DisallowedHost")


if MEDIA_ROOT.startswith("s3://"):
    # media root is a S3 bucket
    MEDIA_BUCKET_URL = urlparse(MEDIA_ROOT)
    STORAGES["default"]["BACKEND"] = "core.storages.CachedS3Storage"
    if MEDIA_BUCKET_URL.path:
        AWS_STORAGE_BUCKET_NAME = MEDIA_BUCKET_URL.path.strip("/")
    else:
        AWS_STORAGE_BUCKET_NAME = MEDIA_BUCKET_URL.hostname
    AWS_PRIVATE_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
    AWS_ACCESS_KEY_ID = MEDIA_BUCKET_URL.username
    AWS_SECRET_ACCESS_KEY = MEDIA_BUCKET_URL.password
    AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", default=None)
    AWS_QUERYSTRING_AUTH = env.bool("AWS_QUERYSTRING_AUTH", default=False)
    AWS_PRIVATE_QUERYSTRING_AUTH = True
    AWS_QUERYSTRING_EXPIRE = env.int("AWS_QUERYSTRING_EXPIRE", default=3600)
    AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", default=None)
    AWS_REGION_NAME = env.str("AWS_REGION_NAME", default=None)
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_FILE_BUFFER_SIZE = 5242880
    # cloudfront singing URLS
    AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN", default=None)
    AWS_CLOUDFRONT_KEY = env.str("AWS_CLOUDFRONT_KEY", default="").encode("ascii")
    AWS_CLOUDFRONT_KEY_ID = env.str("AWS_CLOUDFRONT_KEY_ID", default=None)
    # media convert
    AWS_MEDIACONVERT_QUEUE = env.str("AWS_MEDIACONVERT_QUEUE", default=None)
    AWS_MEDIACONVERT_ROLE = env.str("AWS_MEDIACONVERT_ROLE", default=None)


DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "{{ cookiecutter.project_slug }}/backup"}
DBBACKUP_FILENAME_TEMPLATE = "database-{datetime}.{extension}"
DBBACKUP_MEDIA_FILENAME_TEMPLATE = "media-{datetime}.{extension}"
DBBACKUP_SEND_EMAIL = False


# CRX settings
CRX_DISABLE_ANALYTICS = True
CRX_DISABLE_FOOTER = True
CRX_DISABLE_LAYOUT = True

CRX_FRONTEND_TEMPLATES_PAGES = {
    # templates that are available for all page types
    "*": [
        ("", _("Default")),
    ],
}

CRX_FRONTEND_TEMPLATES_BLOCKS = {
    # templates that are available for all block types
    "*": [
        ("", _("Default")),
    ],
    "cardblock": [
        (
            "coderedcms/blocks/card_block.html",
            _("Card"),
        ),
        (
            "coderedcms/blocks/card_head.html",
            _("Card with header"),
        ),
        (
            "coderedcms/blocks/card_foot.html",
            _("Card with footer"),
        ),
        (
            "coderedcms/blocks/card_head_foot.html",
            _("Card with header and footer"),
        ),
        (
            "coderedcms/blocks/card_blurb.html",
            _("Blurb - rounded image and no border"),
        ),
        (
            "coderedcms/blocks/card_img.html",
            _("Cover image - use image as background"),
        ),
    ],
    "cardgridblock": [
        (
            "coderedcms/blocks/cardgrid_group.html",
            _("Card group - attached cards of equal size"),
        ),
        (
            "coderedcms/blocks/cardgrid_deck.html",
            _("Card deck - separate cards of equal size"),
        ),
        (
            "coderedcms/blocks/cardgrid_columns.html",
            _("Card masonry - fluid brick pattern"),
        ),
    ],
    "basicblock": [
        ("", _("Default")),
        ("website/blocks/content_only_block.html", _("Content only")),
    ],
    "sectionblock": [
        ("", _("Default")),
    ]
}


# develop environment settings
if DEBUG:
    WAGTAIL_CACHE = False

    # allow localhost access
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

    # enable debug toolbar if available
    try:
        import debug_toolbar
    except ModuleNotFoundError:
        pass
    else:
        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
