"""Enrichment service config."""

import os
import pathlib
import sys

from loguru import logger

# project's root
BASE_DIR = pathlib.Path(__file__).parent.parent
DEBUG = bool(int(os.getenv('DEBUG', 1)))

# title of project for Swagger docs
PROJECT_NAME = str(os.getenv('PROJECT_NAME', 'default'))
PROJECT_DESCRIPTION = str(os.getenv('PROJECT_DESCRIPTION', 'default description'))
API_DOC_URL = str(os.getenv('API_DOC_URL', '/api/openapi'))

# settings for paginator
PAG_SIZE_PAGE = int(os.getenv('PAG_PAGE_SIZE', 50))

# auth
AUTH_HOST = str(os.getenv('AUTH_HOST', 'localhost'))
AUTH_PORT = int(os.getenv('AUTH_PORT', 5432))
AUTH_DB = str(os.getenv('AUTH_DB', 'main'))
AUTH_USER = str(os.getenv('AUTH_USER', 'admin'))
AUTH_PASSWORD = str(os.getenv('AUTH_PASSWORD', 'admin'))
AUTH_DSN_ASYNC = (
    f'postgres://{AUTH_USER}:{AUTH_PASSWORD}@{AUTH_HOST}:{AUTH_PORT}/{AUTH_DB}'
)

# movies
MOVIES_HOST = str(os.getenv('MOVIES_HOST', 'localhost'))
MOVIES_PORT = int(os.getenv('MOVIES_PORT', 5432))
MOVIES_DB = str(os.getenv('MOVIES_DB', 'main'))
MOVIES_USER = str(os.getenv('MOVIES_USER', 'admin'))
MOVIES_PASSWORD = str(os.getenv('MOVIES_PASSWORD', 'admin'))
MOVIES_DSN_ASYNC = f'postgres://{MOVIES_USER}:{MOVIES_PASSWORD}@{MOVIES_HOST}:{MOVIES_PORT}/{MOVIES_DB}'

# notifications
NOTIFICATIONS_HOST = str(os.getenv('NOTIFICATIONS_HOST', 'localhost'))
NOTIFICATIONS_PORT = int(os.getenv('NOTIFICATIONS_PORT', 5432))
NOTIFICATIONS_DB = str(os.getenv('NOTIFICATIONS_DB', 'main'))
NOTIFICATIONS_USER = str(os.getenv('NOTIFICATIONS_USER', 'admin'))
NOTIFICATIONS_PASSWORD = str(os.getenv('NOTIFICATIONS_PASSWORD', 'admin'))
NOTIFICATIONS_DSN_ASYNC = f"""postgres://{NOTIFICATIONS_USER}:{NOTIFICATIONS_PASSWORD}@
{NOTIFICATIONS_HOST}:{NOTIFICATIONS_PORT}/{NOTIFICATIONS_DB}"""

EMAIL_SHIPMENT_METHOD = 'email'
SMS_SHIPMENT_METHOD = 'sms'

# ugc
UGC_HOST = str(os.getenv('UGC_HOST', default='localhost'))

# settings for logger
LOG_LEVEL = str(os.getenv('LOG_LEVEL', 'DEBUG'))

# set logger
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)
