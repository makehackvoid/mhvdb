# Django settings for mhvdb project.

# If you have settings that are specific to your local install (like DATABASES
# or paths to templates, etc. then put them in a modify() method in
# local_settings, as shown at http://stackoverflow.com/q/2086802
#
#
# Things which MUST be in local_settings:
#
#def modify(settings):
#        settings['SECRET_KEY'] = 'putrandomstringhere'
#
#for local testing, the settings.py might look like this:
#
# def modify(settings):
#     settings["DATABASES"] = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': '/path/to/mhv.db',
#             }
#         }
#     settings["TEMPLATE_DIRS"] = ( "/path/to/mhvdb/mhvdb/templates/" )
#     settings['SECRET_KEY'] = 'putrandomstringhere'
#     settings['DEBUG'] = True
#     settings['IS_DEVELOPMENT'] = True
#
#
#
# mhv imports
import local_settings
import logging

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mhv.db',
    }
}

# depreciated in django 1.5, should look at using memcached
# on live server
# CACHE_BACKEND = "locmem:///"
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'LOCATION': 'unique-snowflake'
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware', #mhv
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mhvdb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mhvdb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # mhv - set in local_settings.py
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  #mhv
    'members',                  #mhv
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_evolution'
)

### MHV config below here

# This is the membership type that expired or new members default over to
DEFAULT_MEMBERSHIP_NAME = "Casual"  #mhv

# A list of IP networks (can be networks of form 192.168.1.1/24 or
# single IPs, or even IPv6) that are considered "local". Local IP
# Addresses can view the members list, expiry dates, and member
# emergency contact details without being logged in.
#
# Editing content (ie the admin interface) still requires logging in,
# as does viewing any member's details apart from emergency
# contact. Also, the signup form is always available.
#
# The idea is that you add the local LAN network of your organisation,
# so people can quickly view important details.
#
LOCAL_IP_ADDRESSES = []   #mhv

LOGIN_URL = "/login"  #mhv

EMAIL_HOST = "localhost"
EMAIL_PORT = 25

EMAIL_SENDER = "treasurer@makehackvoid.com"

EXPIRING_DAYS = 14 # warn the member when their membership expires this many days away
EXPIRING_INTERNAL_DAYS = 3 # warn the treasurer when a member's membership expires this many days away

EMAIL_SUBJECTS = {
    "welcome.txt"  : "Welcome to Make, Hack, Void!",
    "renewed.txt" : "Make, Hack, Void membership has renewed",
    "expiring.txt" : "Make, Hack, Void membership expires soon",
    "expired.txt"  : "Make, Hack, Void membership has expired",
    "internal.txt" : "MHV membership is about to expire!"
}

EMAIL_CC = {
    "expired.txt" : [ EMAIL_SENDER ],
    "internal.txt" : [ EMAIL_SENDER ], # internal.txt is -only- sent to this address, not to the member
}

IS_DEVELOPMENT = False # override this to =True in local_settings.py for debug/dev servers

# this amount of logging is really only useful for the debug server
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

local_settings.modify(globals())

# Below here is from sample django 1.5 settings.py

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }
