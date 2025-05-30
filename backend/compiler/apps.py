from django.apps import AppConfig

# This class configures the 'compiler' app in the Django project.
class CompilerConfig(AppConfig):
    # Specifies the type of primary key to use for models that don’t define one.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compiler'
