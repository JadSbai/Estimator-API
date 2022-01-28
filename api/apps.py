from django.apps import AppConfig

import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Estimator.settings.development')
