from Estimator.settings.common import *


# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['dry-retreat-95860.herokuapp.com', 'www.dry-retreat-95860.herokuapp.com']

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': os.environ.get('DATABASE_NAME'),
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': os.environ.get('DATABASE_HOST')
            },
        }
    }

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# Activate django heroku
if '/app' in os.environ['HOME']:
    import django_heroku
    django_heroku.settings(locals())