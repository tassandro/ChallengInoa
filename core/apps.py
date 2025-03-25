import os
import atexit
from django.apps import AppConfig

"""
    A função ready() é utilizada para:
    - Registrar automaticamente os signals do Django após as migrações.
    - Agendar a execução da função shutdown_scheduler() ao final da execução do programa.
"""

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Executado quando a aplicação Django é iniciada."""
        from core import signals  # Importa os signals automaticamente

        # Garante que o shutdown do agendador ocorra apenas uma vez
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                from core.scheduler import shutdown_scheduler
                atexit.register(shutdown_scheduler)
            except ImportError as e:
                # Log para facilitar a depuração
                import logging
                logging.error(f"Erro ao importar shutdown_scheduler: {e}")
