import os
import secrets

# Flask settings
# FLASK_SERVER_NAME = FLASK_HOST+":"+str(FLASK_PORT)
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
# Do not use debug mode in production
FLASK_DEBUG = os.environ.get("FLASK_DEBUG") or 'False'
CHATBOT_LOG = "db"
API_URL = os.environ.get("API_URL") or f"http://{FLASK_HOST}:{FLASK_PORT}/api/"
ORIGINS = '*'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# Database settings
DATABASE = os.environ.get("DATABASE_URL") or "sqlite:///dev.db"
# SQLALCHEMY_DATABASE_URI = 'mysql://root:H5hng15K@localhost/skf?charset=utf8mb4'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://foo:bar@35.190.203.79/skf?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

# JWT settings
JWT_ENABLED = os.environ.get("JWT_ENABLED") or 'False'
JWT_SECRET = os.environ.get("JWT_SECRET") or secrets.token_hex(32)

# Google Scraping
GOOGLE = False
API_KEY = os.environ.get("SKF_GOOGLE_API_KEY") or ''
CSE_ID = os.environ.get("SKF_GOOGLE_CSE_ID") or ''

# TESTING settings
TESTING = (os.environ.get("TESTING") == 'True') or False

# RABBIT MQ settings
RABBIT_MQ_CONN_STRING = os.environ.get("RABBIT_MQ_CONN_STRING") or 'localhost'
RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER") or 'guest'
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS") or 'guest'

# SKF-LABS settings
# LABS_KUBE_CONF = os.environ.get("LABS_KUBE_CONF") or '~/.kube/config'
