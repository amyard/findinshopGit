from __future__ import absolute_import

import os
import djcelery

from celery.schedules import crontab
djcelery.setup_loader()

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# FCGI settings
HOST = '127.0.0.1' # http://find.artel7.com
PORT = '8000'#80
METHOD = 'threaded'
ALLOWED_HOSTS = [u'findinshop.com.ua', '*']
FILE_UPLOAD_MAX_MEMORY_SIZE = 5621440

SEARCH_BACKEND = 'sphinx'

BASE_DOMAIN = "localhost:8000"

# CSRF_COOKIE_DOMAIN = 'localhost:8000'
# SESSION_COOKIE_DOMAIN = 'localhost:8000'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

FIXTURE_DIRS = (
    'apps/website/fixtures/',
)

MANAGERS = ADMINS

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/c/s/'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
TEST_GLOBAL_TOP = 'top.document.referer'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    os.path.join(PROJECT_PATH, 'static'),
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6$1b79%5(1zvaz+$thr0wuz7+(jw$f*v9wk#01#b=8y3r^-&amp;@w'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "context_processors.site",
    "context_processors.settings",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'apps.website.middleware.WebsiteSessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.website.middleware.MultiDomainMiddleware',
    #'apps.website.middleware.WebsitePrivateSessionMiddleware',
)

ROOT_URLCONF = 'source.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'source.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),

)


SPHINX_DATABASE_NAME = 'sphinx'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'findinshop',
        'USER': 'findinshop',
        'PASSWORD': 'fargo',
        'HOST': 'localhost',
    },
    'sphinx': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '9306',
    },
}



INSTALLED_APPS = (
    # 'django_sphinx_db',
    #'cacheops',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'djcelery',
    'suit',
    'django.contrib.admin',
    #'django.contrib.admindocs',

    # third party
    # 'south',  # delete
    'mailshelf',
    'categories',
    'categories.editor',
    #'haystack',
    'rest_framework',
    #'sorl.thumbnail',
    'endless_pagination',
    'easy_thumbnails',
    #'flup',
    'social.apps.django_app.default',
    # "push_notifications"

    # on board
    'apps.account',
    'apps.catalog',
    'apps.website',
    'apps.pages',
    'apps.news',
    'apps.version',
    'apps.feedback',
    'apps.ticket',
    'apps.distribution',
    'apps.banner',
    'apps.section',
    'apps.cpa',
    'apps.manager',
    'apps.coupon',
    'apps.dashboard',
    'apps.api_rest'
)

# SOUTH_MIGRATION_MODULES = {
#     'easy_thumbnails': 'easy_thumbnails.south_migrations',
# }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#         },
#         'file_django': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(PROJECT_PATH, 'var/log/django.log'),
#             'maxBytes': '1024',
#             'backupCount': '3'
#         },
#         'file_imega': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(PROJECT_PATH, 'var/log/imega.log'),
#             'maxBytes': '1024',
#             'backupCount': '3'
#         },
#         'file_imegaPB': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(PROJECT_PATH, 'var/log/pb24.log'),
#             'maxBytes': '1024',
#             'backupCount': '3'
#         },
#         'file_sphinx': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(PROJECT_PATH, 'var/log/sphinx_search.log'),
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 3,
#         },
#         'file_importer': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(PROJECT_PATH, 'var/log/importer.log'),
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 3,
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins', 'file_django'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['file_django'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'imega': {
#             'handlers': ['file_imega'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'imegaPB': {
#             'handlers': ['file_imegaPB'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'sphinx_search': {
#             'handlers': ['file_sphinx'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'importer': {
#             'handlers': ['file_importer'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     }
# }


# Celery
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IMPORTS = ("apps.catalog.tasks", )
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    # 'test_schedule': {
    # 'task': 'apps.catalog.tasks.test_schedule',
    #     'schedule': crontab(),
    # },
    # 'delete_items': {
    #     'task': 'apps.catalog.tasks.delete_items',
    #     'schedule': crontab(minute=0, hour=1),
    # },
    'catalog_update': {
        'task': 'apps.catalog.tasks.catalog_update',
        'schedule': crontab(minute=0, hour=1),
    },
    'check_coupons': {
        'task': 'apps.catalog.tasks.check_coupons',
        'schedule': crontab(minute=50, hour=3),
    },
    # 'rebuild_index': {
    #     'task': 'apps.catalog.tasks.index_update',
    #     'schedule': crontab(minute=0, hour=4),
    # },
    'product_search': {
        'task': 'apps.catalog.tasks.product_search',
        'schedule': crontab(minute=50, hour=4),
    },
    'domains': {
        'task': 'apps.catalog.tasks.domains_conf',
        'schedule': crontab(minute=20, hour=5),
    },
}
CELERY_SEND_TASK_ERROR_EMAILS = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'TIMEOUT': 60 * 5,
        'INDEX_NAME': 'ons',
    },
}
#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

ENDLESS_PAGINATION_PER_PAGE = 40

CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    #'db': 1,
    'socket_timeout': 3,
}

CACHEOPS = {
    'catalog.*': ('just_enable', 60*60),
    'feedback.*': ('just_enable', 60*60),
    #'website.*': ('just_enable', 60*60),
    'news.*': ('just_enable', 60*60),
    'pages.*': ('just_enable', 60*60),
    'ticket.*': ('just_enable', 60*60),
    'version.*': ('just_enable', 60*60),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

MANAGER_MAIL = 'tls@1c-bitrix.support' #'tls@findinshop.com'

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CHECK_DOMAINS = False
INSTALLMENT_DOMAIN = 'processing.findinshop.com'

#Sphinx
SPHINX_PATH = "/opt/sphinx"  # for config generation
SPHINX_HOST = 'localhost'
SPHINX_PORT = 9312
SPHINX_INDEX = "product" #,"some_index"
SPHINX_MAX_MATCHES = 10000

REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',)
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.searchservice.com.ua'#'govmail.wishhost.net'
EMAIL_HOST_USER = 'tls@1c-bitrix.support' #'test@artel7.com'
EMAIL_HOST_PASSWORD ='IJTmoBO1TDT@' #'5X5b2B9l'
EMAIL_PORT = 465#587
SERVER_EMAIL = 'tls@1c-bitrix.support'#'test@artel7.com'

search_backend = 'sphinx'
PROXY_FILE_PATH = 'proxy.txt'

GEOIP_FILE_PATH = 'GeoIP.dat'
GEO_LITE_CITY_PATH = 'GeoLiteCity.dat'
GEOCODING_API_KEY = "AIzaSyB4Hh4jy9je_8cXXPeSnTEdcQYzmNm-a-I" #

SESSION_COOKIE_DOMAIN =".%s" % BASE_DOMAIN # ".193.200.173.122"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400 # sec
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_NAME = 'DSESSIONID'
SESSION_COOKIE_SECURE = False

try:
    from source.settings_local import *
except ImportError:
    pass
try:
    from source.settings_registration import *
except ImportError:
    pass
