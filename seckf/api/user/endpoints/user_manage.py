from flask import request
from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha
from seckf.api.user.business import manage_user
from seckf.api.user.parsers import authorization
from seckf.api.user.serializers import manage, message

ns = api.namespace('user', description='Operations related to users')


@ns.route('/manage/<int:id>')
@api.doc(params={'id': 'The user id'})
@api.response(404, 'Validation error', message)
class userManage(Resource):

    @api.expect(authorization, manage)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, id):
        """
        Manage an user.
        * Privileges required: **manage**
        """
        data = request.json
        val_alpha(data.get('active'))
        val_num(id)
        validate_privilege(self, 'manage')
        result = manage_user(id, data)
        return result, 200, security_headers()
