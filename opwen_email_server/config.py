from environs import Env

from opwen_email_server.utils.string import urlsafe

env = Env()

STORAGE_PROVIDER = env('LOKOLE_STORAGE_PROVIDER', 'AZURE_BLOBS')

BLOBS_ACCOUNT = env('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_NAME', '')
BLOBS_KEY = env('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_KEY', '')
BLOBS_HOST = env('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_HOST', '')
BLOBS_SECURE = env.bool('LOKOLE_EMAIL_SERVER_AZURE_BLOBS_SECURE', True)

TABLES_ACCOUNT = env('LOKOLE_EMAIL_SERVER_AZURE_TABLES_NAME', '')
TABLES_KEY = env('LOKOLE_EMAIL_SERVER_AZURE_TABLES_KEY', '')
TABLES_HOST = env('LOKOLE_EMAIL_SERVER_AZURE_TABLES_HOST', '')
TABLES_SECURE = env.bool('LOKOLE_EMAIL_SERVER_AZURE_TABLES_SECURE', True)

CLIENT_STORAGE_ACCOUNT = env('LOKOLE_CLIENT_AZURE_STORAGE_NAME', '')
CLIENT_STORAGE_KEY = env('LOKOLE_CLIENT_AZURE_STORAGE_KEY', '')
CLIENT_STORAGE_HOST = env('LOKOLE_CLIENT_AZURE_STORAGE_HOST', '')
CLIENT_STORAGE_SECURE = env.bool('LOKOLE_CLIENT_AZURE_STORAGE_SECURE', True)

SENDGRID_KEY = env('LOKOLE_SENDGRID_KEY', '')
DNS_ACCOUNT = env('LOKOLE_CLOUDFLARE_USER', '')
DNS_SECRET = env('LOKOLE_CLOUDFLARE_KEY', '')
DNS_PROVIDER = env('LOKOLE_DNS_PROVIDER', 'CLOUDFLARE')

LOG_LEVEL = env('LOKOLE_LOG_LEVEL', 'INFO')

APPINSIGHTS_KEY = env('LOKOLE_EMAIL_SERVER_APPINSIGHTS_KEY', '')
APPINSIGHTS_HOST = env('LOKOLE_EMAIL_SERVER_APPINSIGHTS_HOST', '')

REGISTRATION_USERNAME = env('REGISTRATION_USERNAME', '')
REGISTRATION_PASSWORD = env('REGISTRATION_PASSWORD', '')
REGISTRATION_GITHUB_ORGANIZATION = env('REGISTRATION_GITHUB_ORGANIZATION', 'ascoderu')
REGISTRATION_GITHUB_TEAM = env('REGISTRATION_GITHUB_ORGANIZATION', 'lokole-registration')

MAX_WIDTH_IMAGES = env.int('LOKOLE_MAX_WIDTH_EMAIL_IMAGES', 200)
MAX_HEIGHT_IMAGES = env.int('LOKOLE_MAX_HEIGHT_EMAIL_IMAGES', 200)

if env('LOKOLE_QUEUE_BROKER_SCHEME', '') == 'azureservicebus':
    QUEUE_BROKER = 'azureservicebus://{username}:{password}@{host}'.format(
        username=urlsafe(env('LOKOLE_EMAIL_SERVER_QUEUES_SAS_NAME')),
        password=urlsafe(env('LOKOLE_EMAIL_SERVER_QUEUES_SAS_KEY')),
        host=urlsafe(env('LOKOLE_EMAIL_SERVER_QUEUES_NAMESPACE')))
else:
    QUEUE_BROKER = env('LOKOLE_QUEUE_BROKER_URL', '')
