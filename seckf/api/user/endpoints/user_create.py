from flask import request
from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_alpha_num_special
from seckf.api.user.business import create_user
from seckf.api.user.parsers import authorization
from seckf.api.user.serializers import create, created, message

ns = api.namespace('user', description='Operations related to users')


@ns.route('/create')
@api.response(404, 'Validation error', message)
class userCreation(Resource):

    @api.expect(authorization, create)
    @api.marshal_with(created)
    @api.response(400, 'No results found', message)
    def put(self):
        """
        Create an user.
        * Privileges required: **manage**
        """
        data = request.json
        val_alpha_num_special(data.get('username'))
        val_alpha_num_special(data.get('privilege_id'))
        validate_privilege(self, 'manage')
        result = create_user(data)
        return result, 200, security_headers()
