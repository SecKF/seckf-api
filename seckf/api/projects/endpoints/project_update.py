from flask import request
from flask_restx import Resource

from seckf.api.projects.business import update_project
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import project_update, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha_num_special

ns = api.namespace('project', description='Operations related to projects')


@ns.route('/update/<int:project_id>')
@api.doc(params={'project_id': 'The project id'})
@api.response(404, 'Validation error', message)
class KBItemUpdate(Resource):

    @api.expect(authorization, project_update)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, project_id):
        """
        Update a project item.
        * Privileges required: **edit**
        """
        data = request.json
        val_num(project_id)
        val_alpha_num_special(data.get('name'))
        val_alpha_num_special(data.get('description'))
        val_alpha_num_special(data.get('version'))
        validate_privilege(self, 'edit')
        result = update_project(project_id, data)
        return result, 200, security_headers()
