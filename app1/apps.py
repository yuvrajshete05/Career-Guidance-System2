from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'


from django.apps import AppConfig


class CareerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'career'
