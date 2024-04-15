import os
from .base import *
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default_secret_key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', 'db.sqlite3'),
        # ... other DB settings
    }
}
DEBUG = True

ALLOWED_HOST = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'body_maintenance_main',
        'USER': 'postgres',
        'PASSWORD': 'p@ssw0rd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
 }

# TEMPLATE_PATH='/work/minda/iotfe/UI_new/report_html/'
HTML_DIR_PATH = "/work/minda/iotfe/UI_new/report_html/report_html"
MODULE_NAME = "video_module" 
CSV_PATH ="/work/cummins/smart-security/records/people_record.csv"
TRACEBILITY_DIR_PATH = '/work/minda/iotfe/UI_new/backend/traceability_prod_details/'
APMS_DIR_PATH = '/work/minda/iotfe/UI_new/backend/records/'
BREEAKDOWN_ATTACHMENT_DIR_PATH = "/work/minda/iotfe/attachments"
FNB_REPORT_PATH = "/work/fnb_reports"

DB_HOST = '140.238.167.16'
parent_dir = "/work/minda"

LOGGING ={
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime}  line no {lineno}  {filename} {funcName} {message} ',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/nexgensis/rahul/my_projects/daily_vitality/body_maintenance/UI/iot_apps_logs/iot.log',
            'formatter': 'simple',
            'maxBytes':15*1024*1024, #max 15Mb file
            'backupCount': 5,
            'formatter':'simple',
            'encoding':'utf-8'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'body_maintenance.urls'

# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djangoapp',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@nexgensis.com'
EMAIL_HOST_PASSWORD = 'Welcome#9191'


DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis:http://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"