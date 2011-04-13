from comicbaron.conf.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'comicbaron.conf.dev.urls'

MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'comicbaron',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpassword',
    }
}
