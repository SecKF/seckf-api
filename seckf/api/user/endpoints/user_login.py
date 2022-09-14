from flask import request
from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_alpha_num_special
from seckf.api.user.business import login_user
from seckf.api.user.serializers import login, message, token_auth

ns = api.namespace('user', description='Operations related to users')


@ns.route('/login')
@api.response(404, 'Validation error', message)
class userLogin(Resource):

    @api.expect(login)
    @api.marshal_with(token_auth)
    @api.response(400, 'No results found', token_auth)
    def post(self):
        """
        Login an user.
        * Privileges required: **none**
        """
        data = request.json
        val_alpha_num_special(data.get('username'))
        result = login_user(data)
        return result, 200, security_headers()
