import json
import os

from django.core.exceptions import ImproperlyConfigured

FRONT_END_PORT ='127.0.0.1:3000'

class SettingUtils:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(BASE_DIR, 'earth_de_be/config/config.json')) as secrets_file:
            self.secrets = json.load(secrets_file)

    def get_data(self, setting_key):
        """Get secret setting or fail with ImproperlyConfigured"""
        try:
            return self.secrets[setting_key]
        except KeyError:
            raise ImproperlyConfigured("Set the {} setting".format(setting_key))
