from django.apps import AppConfig


class SigemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sigem"
    # Etiqueta tecnica del aplicativo usada por migraciones, permisos y URLs internas del admin.
    label = "sigem"
    verbose_name = "SIGEM"

