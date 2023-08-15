"""
Django settings for '{{ cookiecutter.project_name }}' project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import environ
import os
from django.utils.translation import gettext_lazy as _
from email.utils import getaddresses
from io import StringIO

BASE_DIR = environ.Path(__file__) - 2
PROJECT_DIR = environ.Path(__file__) - 1

# read enviroment variables
env = environ.Env()
if os.path.isfile(BASE_DIR(".env")):
    env.read_env(BASE_DIR(".env"))

# read .env from enviroment variable
ENV_FILE = env("ENV_FILE", default=None)
if ENV_FILE:
    env.read_env(StringIO(ENV_FILE))

# environment settings
ENVIRONMENT = env("ENVIRONMENT", default="develop")
DEBUG = env.bool("DEBUG", default=True)

# Site URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
VIRTUAL_HOST = env.str("VIRTUAL_HOST", default="localhost")

# secuirty settings
SECRET_KEY = env.str("SECRET_KEY", default="dummy")
INTERNAL_IPS = env.bool("INTERNAL_IPS", default=["127.0.0.1"])
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = "SAMEORIGIN"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[VIRTUAL_HOST])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=[f"https://{VIRTUAL_HOST}"]
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition
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
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
    "wagtail.admin",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # aditional apps
    "storages",
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
    #  Error reporting. Uncomment this to receive emails when a 404 is triggered.
    # 'django.middleware.common.BrokenLinkEmailsMiddleware',
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
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]
STATIC_ROOT = env("STATIC_ROOT", default=BASE_DIR("staticfiles"))
STATIC_URL = env("STATIC_URL", default="/static/")

# {% if cookiecutter.whitenoise_static %}
# Whitenoiise
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# {% endif %}

# {% if cookiecutter.sass %}
# SASS preprocessor
COMPRESS_OFFLINE = True
SASS_PROCESSOR_AUTO_INCLUDE = True
SASS_OUTPUT_STYLE = "compact"
# {% endif %}

# Media files
MEDIA_ROOT = env("MEDIA_ROOT", default=BASE_DIR("media"))
MEDIA_URL = env("MEDIA_URL", default="/media/")
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024**2  # max upload data 20 MB
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
WAGTAIL_I18N_ENABLED = False
WAGTAILADMIN_COMMENTS_ENABLED = False
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 8 * 1024**2  # 8 MB
WAGTAILADMIN_BASE_URL = f"https://{VIRTUAL_HOST}"

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

# sentry error reporter
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:  # sentry is configured
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration, RedisIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), RedisIntegration()],
        environment=ENVIRONMENT,
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

# S3 emdia baucket
S3_MEDIA_BUCKET_URL = env.url("S3_MEDIA_BUCKET_URL", default=None)
if S3_MEDIA_BUCKET_URL:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_PRIVATE_QUERYSTRING_AUTH = True
    AWS_ACCESS_KEY_ID = S3_MEDIA_BUCKET_URL.username
    AWS_SECRET_ACCESS_KEY = S3_MEDIA_BUCKET_URL.password
    AWS_STORAGE_BUCKET_NAME = S3_MEDIA_BUCKET_URL.path.strip("/")
    AWS_PRIVATE_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
    AWS_QUERYSTRING_EXPIRE = 3600

# CRX TEAMPLTES
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
