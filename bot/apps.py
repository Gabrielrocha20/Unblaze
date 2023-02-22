from django.apps import AppConfig
from utils.request_api import start_thread


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        start_thread()
