from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eCommerce'
    
    # def ready(self):
    #     from django.core.management import call_command
    #     call_command('loaddata', 'data.json')

    #  python manage.py loaddata data.json
