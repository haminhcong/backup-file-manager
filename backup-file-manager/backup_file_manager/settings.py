import os
import platform
import warnings

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

#
# Environment setup
#

VERSION = '1.0.0-dev'

# Hostname
HOSTNAME = platform.node()

# Set the base directory two levels up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Validate Python version
if platform.python_version_tuple() < ('3', '6'):
    raise RuntimeError(
        "Backup File Manager requires Python 3.6 or higher (current: Python {})".format(platform.python_version())
    )

#
# Configuration import
#

# Import configuration parameters
try:
    from backup_file_manager import configuration
except ImportError:
    raise ImproperlyConfigured(
        "Configuration file is not present. Please define "
        "backup_file_manager/backup_file_manager/configuration.py per the documentation."
    )

# Enforce required configuration parameters
for parameter in ['ALLOWED_HOSTS', 'DATABASE', 'SECRET_KEY']:
    if not hasattr(configuration, parameter):
        raise ImproperlyConfigured(
            "Required parameter {} is missing from configuration.py.".format(parameter)
        )

# Set required parameters
ALLOWED_HOSTS = getattr(configuration, 'ALLOWED_HOSTS')
DATABASE = getattr(configuration, 'DATABASE')
SECRET_KEY = getattr(configuration, 'SECRET_KEY')

# Set optional parameters
ADMINS = getattr(configuration, 'ADMINS', [])
ALLOWED_URL_SCHEMES = getattr(configuration, 'ALLOWED_URL_SCHEMES', (
    'file', 'ftp', 'ftps', 'http', 'https', 'irc', 'mailto', 'sftp', 'ssh', 'tel', 'telnet', 'tftp', 'vnc', 'xmpp',
))
BANNER_BOTTOM = getattr(configuration, 'BANNER_BOTTOM', '')
BANNER_LOGIN = getattr(configuration, 'BANNER_LOGIN', '')
BANNER_TOP = getattr(configuration, 'BANNER_TOP', '')
BASE_PATH = getattr(configuration, 'BASE_PATH', '')
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip('/') + '/'  # Enforce trailing slash only
CACHE_TIMEOUT = getattr(configuration, 'CACHE_TIMEOUT', 900)
CHANGELOG_RETENTION = getattr(configuration, 'CHANGELOG_RETENTION', 90)
CORS_ORIGIN_ALLOW_ALL = getattr(configuration, 'CORS_ORIGIN_ALLOW_ALL', False)
CORS_ORIGIN_REGEX_WHITELIST = getattr(configuration, 'CORS_ORIGIN_REGEX_WHITELIST', [])
CORS_ORIGIN_WHITELIST = getattr(configuration, 'CORS_ORIGIN_WHITELIST', [])
DATE_FORMAT = getattr(configuration, 'DATE_FORMAT', 'N j, Y')
DATETIME_FORMAT = getattr(configuration, 'DATETIME_FORMAT', 'N j, Y g:i a')
DEBUG = getattr(configuration, 'DEBUG', False)
DEVELOPER = getattr(configuration, 'DEVELOPER', False)
DOCS_ROOT = getattr(configuration, 'DOCS_ROOT', os.path.join(os.path.dirname(BASE_DIR), 'docs'))
EMAIL = getattr(configuration, 'EMAIL', {})
ENFORCE_GLOBAL_UNIQUE = getattr(configuration, 'ENFORCE_GLOBAL_UNIQUE', False)
EXEMPT_VIEW_PERMISSIONS = getattr(configuration, 'EXEMPT_VIEW_PERMISSIONS', [])
HTTP_PROXIES = getattr(configuration, 'HTTP_PROXIES', None)
INTERNAL_IPS = getattr(configuration, 'INTERNAL_IPS', ('127.0.0.1', '::1'))
LOGGING = getattr(configuration, 'LOGGING', {})
LOGIN_REQUIRED = getattr(configuration, 'LOGIN_REQUIRED', False)
LOGIN_TIMEOUT = getattr(configuration, 'LOGIN_TIMEOUT', None)
MAINTENANCE_MODE = getattr(configuration, 'MAINTENANCE_MODE', False)
MAX_PAGE_SIZE = getattr(configuration, 'MAX_PAGE_SIZE', 1000)
MEDIA_ROOT = getattr(configuration, 'MEDIA_ROOT', os.path.join(BASE_DIR, 'media')).rstrip('/')
STORAGE_BACKEND = getattr(configuration, 'STORAGE_BACKEND', None)
STORAGE_CONFIG = getattr(configuration, 'STORAGE_CONFIG', {})
METRICS_ENABLED = getattr(configuration, 'METRICS_ENABLED', False)
PAGINATE_COUNT = getattr(configuration, 'PAGINATE_COUNT', 50)
PLUGINS = getattr(configuration, 'PLUGINS', [])
PLUGINS_CONFIG = getattr(configuration, 'PLUGINS_CONFIG', {})
PREFER_IPV4 = getattr(configuration, 'PREFER_IPV4', False)
REPORTS_ROOT = getattr(configuration, 'REPORTS_ROOT', os.path.join(BASE_DIR, 'reports')).rstrip('/')
SCRIPTS_ROOT = getattr(configuration, 'SCRIPTS_ROOT', os.path.join(BASE_DIR, 'scripts')).rstrip('/')
SESSION_FILE_PATH = getattr(configuration, 'SESSION_FILE_PATH', None)
SHORT_DATE_FORMAT = getattr(configuration, 'SHORT_DATE_FORMAT', 'Y-m-d')
SHORT_DATETIME_FORMAT = getattr(configuration, 'SHORT_DATETIME_FORMAT', 'Y-m-d H:i')
SHORT_TIME_FORMAT = getattr(configuration, 'SHORT_TIME_FORMAT', 'H:i:s')
TIME_FORMAT = getattr(configuration, 'TIME_FORMAT', 'g:i a')
TIME_ZONE = getattr(configuration, 'TIME_ZONE', 'UTC')

#
# Database
#

# Only PostgreSQL is supported
if METRICS_ENABLED:
    DATABASE.update({
        'ENGINE': 'django_prometheus.db.backends.postgresql'
    })
else:
    DATABASE.update({
        'ENGINE': 'django.db.backends.postgresql'
    })

DATABASES = {
    'default': DATABASE,
}

#
# Media storage
#

if STORAGE_BACKEND is not None:
    DEFAULT_FILE_STORAGE = STORAGE_BACKEND

    # django-storages
    if STORAGE_BACKEND.startswith('storages.'):

        try:
            import storages.utils
        except ImportError:
            raise ImproperlyConfigured(
                "STORAGE_BACKEND is set to {} but django-storages is not present. It can be installed by running 'pip "
                "install django-storages'.".format(STORAGE_BACKEND)
            )

        # Monkey-patch django-storages to fetch settings from STORAGE_CONFIG
        def _setting(name, default=None):
            if name in STORAGE_CONFIG:
                return STORAGE_CONFIG[name]
            return globals().get(name, default)


        storages.utils.setting = _setting

if STORAGE_CONFIG and STORAGE_BACKEND is None:
    warnings.warn(
        "STORAGE_CONFIG has been set in configuration.py but STORAGE_BACKEND is not defined. STORAGE_CONFIG will be "
        "ignored."
    )

#
# Sessions
#

if LOGIN_TIMEOUT is not None:
    # Django default is 1209600 seconds (14 days)
    SESSION_COOKIE_AGE = LOGIN_TIMEOUT
if SESSION_FILE_PATH is not None:
    SESSION_ENGINE = 'django.contrib.sessions.backends.file'

#
# Email
#

EMAIL_HOST = EMAIL.get('SERVER')
EMAIL_HOST_USER = EMAIL.get('USERNAME')
EMAIL_HOST_PASSWORD = EMAIL.get('PASSWORD')
EMAIL_PORT = EMAIL.get('PORT', 25)
EMAIL_SSL_CERTFILE = EMAIL.get('SSL_CERTFILE')
EMAIL_SSL_KEYFILE = EMAIL.get('SSL_KEYFILE')
EMAIL_SUBJECT_PREFIX = '[Backup File Manager] '
EMAIL_USE_SSL = EMAIL.get('USE_SSL', False)
EMAIL_USE_TLS = EMAIL.get('USE_TLS', False)
EMAIL_TIMEOUT = EMAIL.get('TIMEOUT', 10)
SERVER_EMAIL = EMAIL.get('FROM_EMAIL')

#
# Django
#

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'debug_toolbar',
    'django_filters',
    'django_tables2',
    'django_prometheus',
    'rest_framework',
    'timezone_field',
    'file_manager',
    'users',
    'extras',
    'utilities',
    'drf_yasg',
]

# Middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'utilities.middleware.ExceptionHandlingMiddleware',
    'utilities.middleware.LoginRequiredMiddleware',
    'utilities.middleware.APIVersionMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'backup_file_manager.urls'

TEMPLATES_DIR = BASE_DIR + '/templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utilities.context_processors.settings_and_registry',
            ],
        },
    },
]

# Set up authentication backends
AUTHENTICATION_BACKENDS = [
    'backup_file_manager.authentication.ObjectPermissionBackend',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True

# WSGI
WSGI_APPLICATION = 'backup_file_manager.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/{}static/'.format(BASE_PATH)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "project-static"),
)

# Media
MEDIA_URL = '/{}media/'.format(BASE_PATH)

# Disable default limit of 1000 fields per request. Needed for bulk deletion of objects. (Added in Django 1.10.)
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Authentication URLs
LOGIN_URL = '/{}login/'.format(BASE_PATH)

CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

# Exclude potentially sensitive models from wildcard view exemption. These may still be exempted
# by specifying the model individually in the EXEMPT_VIEW_PERMISSIONS configuration parameter.
EXEMPT_EXCLUDE_MODELS = (
    ('auth', 'group'),
    ('auth', 'user'),
    ('users', 'objectpermission'),
)

#
# Django Prometheus
#

PROMETHEUS_EXPORT_MIGRATIONS = False

#
# Django filters
#

FILTERS_NULL_CHOICE_LABEL = 'None'
FILTERS_NULL_CHOICE_VALUE = 'null'

#
# Django REST framework (API)
#

REST_FRAMEWORK_VERSION = VERSION.rsplit('.', 1)[0]  # Use major.minor as API version
REST_FRAMEWORK = {
    'ALLOWED_VERSIONS': [REST_FRAMEWORK_VERSION],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'backup_file_manager.api.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'backup_file_manager.api.OptionalLimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'backup_file_manager.api.TokenPermissions',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'backup_file_manager.api.FormlessBrowsableAPIRenderer',
    ),
    'DEFAULT_VERSION': REST_FRAMEWORK_VERSION,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'PAGE_SIZE': PAGINATE_COUNT,
    'VIEW_NAME_FUNCTION': 'backup_file_manager.api.get_view_name',
}

#
# drf_yasg (OpenAPI/Swagger)
#

SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'utilities.custom_inspectors.BackupFileManagerSwaggerAutoSchema',
    'DEFAULT_FIELD_INSPECTORS': [
        'utilities.custom_inspectors.JSONFieldInspector',
        'utilities.custom_inspectors.NullableBooleanFieldInspector',
        'utilities.custom_inspectors.CustomChoiceFieldInspector',
        'utilities.custom_inspectors.SerializedPKRelatedFieldInspector',
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.ReferencingSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
    'DEFAULT_FILTER_INSPECTORS': [
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ],
    'DEFAULT_INFO': 'backup_file_manager.urls.openapi_info',
    'DEFAULT_MODEL_DEPTH': 1,
    'DEFAULT_PAGINATOR_INSPECTORS': [
        'utilities.custom_inspectors.NullablePaginatorInspector',
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ],
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
    'VALIDATOR_URL': None,
}

#
# backup file manager internal settings
#

# Secrets
SECRETS_MIN_PUBKEY_SIZE = 2048

# Pagination
PER_PAGE_DEFAULTS = [
    25, 50, 100, 250, 500, 1000
]
if PAGINATE_COUNT not in PER_PAGE_DEFAULTS:
    PER_PAGE_DEFAULTS.append(PAGINATE_COUNT)
    PER_PAGE_DEFAULTS = sorted(PER_PAGE_DEFAULTS)
