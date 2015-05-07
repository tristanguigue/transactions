"""
Django settings for houseprice project.
"""
SECRET_KEY = 'm0j-_$f+9o(c*hp#$h&u-)$xqq%xz8gyt1ym3#@%8#q8(=8eh)'

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'housepriceapp',
    'rest_framework',
    'djangobower',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'houseprice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'houseprice.wsgi.application'

# API
REST_FRAMEWORK = {
    'PAGE_SIZE': 400,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://tristanguigue@localhost:5432/tristanguigue')
}

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'components'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
