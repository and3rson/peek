from common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'notes',
        'HOST': 'localhost',
        'PORT': 5432,
        'USER': 'anderson',
        'PASS': '',
    }
}
