#########################
#                       #
#   Required settings   #
#                       #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the server. This service will not permit write
# access to the server via any other hostnames. The first FQDN in the list will be treated as the preferred name.
#
# Example: ALLOWED_HOSTS = ['service.example.com', 'service.internal.local']
ALLOWED_HOSTS = []

# PostgreSQL database configuration. See the Django documentation for a complete list of available parameters:
#   https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASE = {
    'NAME': 'backup_file_manager',         # Database name
    'USER': '',               # PostgreSQL username
    'PASSWORD': '',           # PostgreSQL password
    'HOST': 'localhost',      # Database server
    'PORT': '',               # Database port (leave blank for default)
    'CONN_MAX_AGE': 300,      # Max database connection age
}

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. This service will not run without this defined. For more information, see
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = ''


#########################
#                       #
#   Optional settings   #
#                       #
#########################

# Specify one or more name and email address tuples representing Service administrators.
# These people will be notified of application errors (assuming correct email settings are provided).
ADMINS = [
    # ['John Doe', 'jdoe@example.com'],
]

# URL schemes that are allowed within links in this Service
ALLOWED_URL_SCHEMES = (
    'file', 'ftp', 'ftps', 'http', 'https', 'irc', 'mailto', 'sftp', 'ssh', 'tel', 'telnet', 'tftp', 'vnc', 'xmpp',
)

# Optionally display a persistent banner at the top and/or bottom of every page. HTML is allowed. To display the same
# content in both banners, define BANNER_TOP and set BANNER_BOTTOM = BANNER_TOP.
BANNER_TOP = ''
BANNER_BOTTOM = ''

# Text to include on the login page above the login form. HTML is allowed.
BANNER_LOGIN = ''

# Base URL path if accessing Backup File Manager within a directory. For example, if installed at
# http://example.com/backup-file-manager/, set:
# BASE_PATH = 'backup-file-manager/'
BASE_PATH = ''

# Cache timeout in seconds. Set to 0 to disable caching. Defaults to 900 (15 minutes)
CACHE_TIMEOUT = 900

# Maximum number of days to retain logged changes. Set to 0 to retain changes indefinitely. (Default: 90)
CHANGELOG_RETENTION = 90

# API Cross-Origin Resource Sharing (CORS) settings. If CORS_ORIGIN_ALLOW_ALL is set to True, all origins will be
# allowed. Otherwise, define a list of allowed origins using either CORS_ORIGIN_WHITELIST or
# CORS_ORIGIN_REGEX_WHITELIST. For more information, see https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # 'https://hostname.example.com',
]
CORS_ORIGIN_REGEX_WHITELIST = [
    # r'^(https?://)?(\w+\.)?example\.com$',
]

# Set to True to enable server debugging. WARNING: Debugging introduces a substantial performance penalty and may reveal
# sensitive information about your installation. Only enable debugging while performing testing. Never enable debugging
# on a production system.
DEBUG = False

# Email settings
EMAIL = {
    'SERVER': 'localhost',
    'PORT': 25,
    'USERNAME': '',
    'PASSWORD': '',
    'USE_SSL': False,
    'USE_TLS': False,
    'TIMEOUT': 10,  # seconds
    'FROM_EMAIL': '',
}

# Enforcement of unique IP space can be toggled on a per-VRF basis. To enforce unique IP space within the global table
# (all prefixes and IP addresses not assigned to a VRF), set ENFORCE_GLOBAL_UNIQUE to True.
ENFORCE_GLOBAL_UNIQUE = False

# Exempt certain models from the enforcement of view permissions. Models listed here will be viewable by all users and
# by anonymous users. List models in the form `<app>.<model>`. Add '*' to this list to exempt all models.
EXEMPT_VIEW_PERMISSIONS = [
    # 'dcim.site',
    # 'dcim.region',
    # 'ipam.prefix',
]

# HTTP proxies Backup File Manager should use when sending outbound HTTP requests (e.g. for webhooks).
# HTTP_PROXIES = {
#     'http': 'http://10.10.1.10:3128',
#     'https': 'http://10.10.1.10:1080',
# }

# IP addresses recognized as internal to the system. The debugging toolbar will be available only to clients accessing
# Backup File Manager from an internal IP.
INTERNAL_IPS = ('127.0.0.1', '::1')

# Enable custom logging. Please see the Django documentation for detailed guidance on configuring custom logs:
#   https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {}

# Setting this to True will permit only authenticated users to access any part of Backup File Manager.
# By default, anonymous users
# are permitted to access most data in Backup File Manager (excluding secrets) but not make any changes.
LOGIN_REQUIRED = False

# The length of time (in seconds) for which a user will remain logged into the web UI before being prompted to
# re-authenticate. (Default: 1209600 [14 days])
LOGIN_TIMEOUT = None

# Setting this to True will display a "maintenance mode" banner at the top of every page.
MAINTENANCE_MODE = False

# An API consumer can request an arbitrary number of objects =by appending the "limit" parameter to the URL (e.g.
# "?limit=1000"). This setting defines the maximum limit. Setting it to 0 or None will allow an API consumer to request
# all objects by specifying "?limit=0".
MAX_PAGE_SIZE = 1000

# The file path where uploaded media such as image attachments are stored. A trailing slash is not needed. Note that
# the default value of this setting is derived from the installed location.
# MEDIA_ROOT = '/opt/backup-file-manager/media'

# By default uploaded media is stored on the local filesystem. Using Django-storages is also supported. Provide the
# class path of the storage driver in STORAGE_BACKEND and any configuration options in STORAGE_CONFIG. For example:
# STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'
# STORAGE_CONFIG = {
#     'AWS_ACCESS_KEY_ID': 'Key ID',
#     'AWS_SECRET_ACCESS_KEY': 'Secret',
#     'AWS_STORAGE_BUCKET_NAME': 'backup-file-manager',
#     'AWS_S3_REGION_NAME': 'eu-west-1',
# }

# Expose Prometheus monitoring metrics at the HTTP endpoint '/metrics'
METRICS_ENABLED = False

# Determine how many objects to display per page within a list. (Default: 50)
PAGINATE_COUNT = 50

SESSION_FILE_PATH = None

# Time zone (default: UTC)
TIME_ZONE = 'UTC'

# Date/time formatting. See the following link for supported formats:
# https://docs.djangoproject.com/en/stable/ref/templates/builtins/#date
DATE_FORMAT = 'N j, Y'
SHORT_DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'g:i a'
SHORT_TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'N j, Y g:i a'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
