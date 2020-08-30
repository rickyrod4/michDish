from django.apps import AppConfig
from  django.db.models.signals import post_save


class RecipesConfig(AppConfig):
    name = 'dish'
    verbose_name = 'MichDish'

    def ready(self):
        print('DISH APP READY')
        from . import signals
