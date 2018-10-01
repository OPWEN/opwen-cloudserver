from os import environ

STORAGE_PROVIDER = environ.get('LOKOLE_STORAGE_PROVIDER', 'AZURE_BLOBS')
BLOBS_ACCOUNT = environ.get('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_NAME', '')
BLOBS_KEY = environ.get('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_KEY', '')
TABLES_ACCOUNT = environ.get('LOKOLE_EMAIL_SERVER_AZURE_TABLES_NAME', '')
TABLES_KEY = environ.get('LOKOLE_EMAIL_SERVER_AZURE_TABLES_KEY', '')

CLIENT_STORAGE_ACCOUNT = environ.get('LOKOLE_CLIENT_AZURE_STORAGE_NAME', '')
CLIENT_STORAGE_KEY = environ.get('LOKOLE_CLIENT_AZURE_STORAGE_KEY', '')

EMAIL_SENDER_KEY = environ.get('LOKOLE_SENDGRID_KEY', '')

LOG_LEVEL = environ.get('LOKOLE_LOG_LEVEL', 'DEBUG')

APPINSIGHTS_KEY = environ.get('LOKOLE_EMAIL_SERVER_APPINSIGHTS_KEY', '')

MAX_WIDTH_IMAGES = int(environ.get('MAX_WIDTH_EMAIL_IMAGES', '200'))
MAX_HEIGHT_IMAGES = int(environ.get('MAX_HEIGHT_EMAIL_IMAGES', '200'))

CELERY_BROKER = environ.get('CELERY_BROKER_URL') or (
    '{scheme}://{username}:{password}@{host}'.format(
        scheme=environ.get('CELERY_BROKER_SCHEME'),
        username=environ.get('CELERY_BROKER_USERNAME'),
        password=environ.get('CELERY_BROKER_PASSWORD'),
        host=environ.get('CELERY_BROKER_HOST')))
