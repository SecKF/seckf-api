from flask_restx import Resource

from seckf.api.projects.business import delete_project
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('project', description='Operations related to project items')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The project id'})
@api.response(404, 'Validation error', message)
class ProjectItemDelete(Resource):
    @api.expect(authorization)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Deletes project item.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_project(id)
        return result, 200, security_headers()
