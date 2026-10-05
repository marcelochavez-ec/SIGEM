from django.apps import AppConfig


class SigesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "siges"
    # Etiqueta tecnica del aplicativo usada por migraciones, permisos y URLs internas del admin.
    label = "siges"
    verbose_name = "SIGES"

