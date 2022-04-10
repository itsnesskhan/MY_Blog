from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'Myapp'

    def ready(self):
        import Myapp.signals
