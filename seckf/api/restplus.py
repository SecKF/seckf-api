import logging

from flask_restx import Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from seckf import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='OWASP-SKF API', description='OWASP-SKF Flask RestPlus powered API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    # log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 400


@api.errorhandler(IntegrityError)
def database_integrity_error_handler(e):
    # log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 400
