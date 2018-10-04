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

if environ.get('QUEUE_BROKER_SCHEME') == 'azureservicebus':
    QUEUE_BROKER = 'azureservicebus://{username}:{password}@{host}'.format(
        username=environ.get('LOKOLE_EMAIL_SERVER_QUEUES_SAS_NAME'),
        password=environ.get('LOKOLE_EMAIL_SERVER_QUEUES_SAS_KEY'),
        host=environ.get('LOKOLE_EMAIL_SERVER_QUEUES_NAMESPACE'))
else:
    QUEUE_BROKER = environ.get('QUEUE_BROKER_URL', '')
