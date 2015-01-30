from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'logan',
        'PASSWORD': '1234',
#       'NAME': os.path.join(BASE_DIR, 'sarvahar'),
        'NAME': 'sarvahar',
    }
}
