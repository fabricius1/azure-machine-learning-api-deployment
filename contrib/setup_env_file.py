from django.core.management.utils import get_random_secret_key
import random
import sys


# SETUP .env file
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

if len(sys.argv) == 1:
    azure_web_app_name = "".join([random.choice(chars) for x in range(15)])
elif len(sys.argv) == 2:
    azure_web_app_name = sys.argv[1]
else:
    raise TypeError('zero or one command line arguments were expected, '
                    f'got {len(sys.argv)}')

ENV_STRING = f"""
AZURE_WEB_APP_NAME=django-app-{azure_web_app_name}
DEBUG=False
SECRET_KEY={get_random_secret_key()}
ALLOWED_HOSTS=127.0.0.1, .localhost, 0.0.0.0, django-app-{azure_web_app_name}.azurewebsites.net
""".strip()

with open('.env', 'w') as file:
    file.write(ENV_STRING)



