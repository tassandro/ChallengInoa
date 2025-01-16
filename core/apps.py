import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals  # Importa os signals automaticamente
        if os.environ.get('RUN_MAIN', None) != 'true':
            # Importa e executa o agendador
            from core.scheduler import shutdown_scheduler
            import atexit
            atexit.register(shutdown_scheduler)
