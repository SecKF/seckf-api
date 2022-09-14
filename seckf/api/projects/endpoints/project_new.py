from flask import request
from flask_restx import Resource

from seckf.api.projects.business import new_project
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import project_new, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege, select_userid_jwt
from seckf.api.security import val_alpha_num, val_alpha_num_special

ns = api.namespace('project', description='Operations related to project items')


@ns.route('/new')
@api.response(404, 'Validation error', message)
class ProjectItemNew(Resource):

    @api.expect(authorization, project_new)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self):
        """
        Create new project item.
        * Privileges required: **edit**
        """
        data = request.json
        val_alpha_num_special(data.get('name'))
        val_alpha_num(data.get('version'))
        val_alpha_num_special(data.get('description'))
        validate_privilege(self, 'edit')
        user_id = select_userid_jwt(self)
        result = new_project(user_id, data)
        return result, 200, security_headers()
