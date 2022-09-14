"""Settings module for test app."""

ENV = "development"
TESTING = True
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
# SQLALCHEMY_DATABASE_URI = "sqlite:///../test.db"
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = (
    4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
)
DEBUG_TB_ENABLED = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False

SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTX_ERROR_404_HELP = False
ORIGINS = '*'

REGENERATE_DATABASE = True
GOOGLE = False
