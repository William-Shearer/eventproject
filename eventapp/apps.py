from django.apps import AppConfig

class EventappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventapp'

    def ready(self):
        from .updater import executeupdate
        executeupdate.execute()
