from dotenv import load_dotenv
load_dotenv()

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_KEY'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.buratovich.com','buratovich.com', '127.0.0.1', '200.32.43.43']

ADMINS = [('Luciano Muñoz', 'hola@luciano.im'),]
MANAGERS = [('Luciano Muñoz', 'hola@luciano.im'),]

# Application definition

INSTALLED_APPS = [
    'admin_reorder',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mathfilters',
    'debug_toolbar',
    'tinymce',
    'el_pagination',
    'website.apps.WebsiteConfig',
    'extranet.apps.ExtranetConfig'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Translation middleware
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'bh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'apptemplates.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'bh.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': 60,
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGES = [
    ('es', 'ESP'),
    ('en', 'ENG'),
    ('pt', 'POR'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

# This work if USE_L10N is set to True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
DECIMAL_SEPARATOR = ','

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# Redirect to this URL when try to access unauthorized user to extranet URL
LOGIN_URL = '/login/requerido/'
# Redirect to this URL after login
LOGIN_REDIRECT_URL = '/extranet/'
# Redirect to this URL after logout
LOGOUT_REDIRECT_URL = '/'


# EMAIL Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

SERVER_EMAIL = 'website@buratovich.com'


# REMOTE SERVER
RS_HOST = os.getenv('RS_HOST')
RS_PORT = os.getenv('RS_PORT')
RS_USER = os.getenv('RS_USER')
RS_PASS = os.getenv('RS_PASS')


# Extranet files
EXTRANET_DIR = os.getenv('FTP_DIR')


# Security Settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'SAMEORIGIN'


#Token Lifetime
PASSWORD_RESET_TIMEOUT_DAYS = 360


# Use this backend to support is_active flag
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']


# Django Debug Toolbar Settings
INTERNAL_IPS = [
    '127.0.0.1',
]


# Django-tinymce Settings
# TINYMCE_DEFAULT_CONFIG = {
# 	'theme': 'advanced',
# 	'theme_advanced_buttons1': 'bold,italic,underline,separator,bullist,numlist,separator,link,unlink',
# 	'theme_advanced_buttons2': '',
# 	'theme_advanced_buttons3': '',
# 	'theme_advanced_toolbar_location': 'top',
# 	'theme_advanced_toolbar_align': 'left',
# }
TINYMCE_COMPRESSOR = True


# Django El Pagination
EL_PAGINATION_PER_PAGE = 100


ADMIN_REORDER = (
    {'app': 'admin_interface', 'models': ('admin_interface.Theme',)},
    {'app': 'auth', 'models': ('auth.User', 'auth.Group')},
    {'app': 'website', 'models': ('website.Currencies', 'website.Board'), 'label': 'Moneda y Pizarras'},
    {'app': 'website', 'models': ('website.City', 'website.Rain'), 'label': 'Lluvias'},
    {'app': 'extranet', 'models': ('website.Notifications', 'website.ViewedNotifications'), 'label': 'Notificaciones'},
    {'app': 'website', 'models': ('website.Careers',), 'label': 'Busquedas Laborales'},
    {'app': 'extranet', 'models': ('website.AccessLog',), 'label': 'Accesos'},
)


# Source of Quality data = 'ticket_analysis' | 'income_quality'
SOURCE_QUALITY_DATA = 'ticket_analysis'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
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


# Settings configured when upgrade to Django 4
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'