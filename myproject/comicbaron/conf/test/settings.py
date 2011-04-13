from comicbaron.conf.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = 'comicbaron.conf.test.urls'

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
