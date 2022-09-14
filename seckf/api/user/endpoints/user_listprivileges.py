from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.user.business import list_privileges
from seckf.api.user.parsers import authorization
from seckf.api.user.serializers import privilege_items, message

ns = api.namespace('user', description='Operations related to users')


@ns.route('/list_privileges')
@api.response(404, 'Validation error', message)
class userListPrivileges(Resource):

    @api.expect(authorization)
    @api.marshal_with(privilege_items)
    @api.response(400, 'No results found', message)
    def get(self):
        """
        List available users.
        * Privileges required: **manage**
        """
        validate_privilege(self, 'manage')
        result = list_privileges()
        return result, 200, security_headers()
