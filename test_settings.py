"""
test settings
"""

import os
from django.utils.translation import ugettext_lazy as _
# BASE_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

SECRET_KEY = 'secret_for_testing_only'
LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

STANDALONE = True

DEBUG = True

FIXTURE_DIRS = (
   '%s/retirement_api/fixtures/' % PROJECT_PATH,
)

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    '%s/retirement_api/templates' % PROJECT_PATH,
    )

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'retirement_api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'retirement_api.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'retire.db'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/retirement/static/'
STATIC_ROOT = '%s/retirement_api/static/' % PROJECT_PATH
