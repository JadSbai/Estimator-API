from Estimator.settings.common import *

SECRET_KEY = 'django-insecure-j0yj%p0vn4)o*v)xxo@y*2%ht0efatb^3n#jh=08i=t)^d8(%s'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'local_estimator_db',
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': 'mongodb+srv://Jad:ZORO@cluster0.q65kn.mongodb.net/test?authSource=admin&replicaSet=atlas-wk045q-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'
            },
        }
    }