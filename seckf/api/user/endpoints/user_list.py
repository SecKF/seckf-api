from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.user.business import list_users
from seckf.api.user.parsers import authorization
from seckf.api.user.serializers import user_items, message

ns = api.namespace('user', description='Operations related to users')


@ns.route('/list')
@api.response(404, 'Validation error', message)
class userList(Resource):

    @api.expect(authorization)
    @api.marshal_with(user_items)
    @api.response(400, 'No results found', message)
    def get(self):
        """
        List available users.
        * Privileges required: **manage**
        """
        validate_privilege(self, 'manage')
        result = list_users()
        return result, 200, security_headers()
