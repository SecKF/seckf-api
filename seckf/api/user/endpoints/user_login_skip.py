from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.user.business import login_skip
from seckf.api.user.serializers import message, token_auth

ns = api.namespace('user', description='Operations related to users')


@ns.route('/skip')
@api.response(404, 'Validation error', message)
class userSkip(Resource):

    @api.marshal_with(token_auth)
    @api.response(400, 'No results found', token_auth)
    def get(self):
        """
        Login an anonymous user.
        * Privileges required: **none**
        """
        result = login_skip()
        return result, 200, security_headers()
