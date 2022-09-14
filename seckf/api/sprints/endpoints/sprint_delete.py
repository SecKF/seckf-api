from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num
from seckf.api.sprints.business import delete_sprint
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import message

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The sprint id'})
@api.response(404, 'Validation error', message)
class ProjectSprintItemDelete(Resource):

    @api.expect(authorization)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Deletes sprint item.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_sprint(id)
        return result, 200, security_headers()
