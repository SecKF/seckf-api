from flask import request
from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha_num_special
from seckf.api.sprints.business import update_sprint
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import sprint_update, message

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/update/<int:id>')
@api.doc(params={'id': 'The sprint id'})
@api.response(404, 'Validation error', message)
class ProjectSprintItemUpdate(Resource):

    @api.expect(authorization, sprint_update)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, id):
        """
        Update a sprint item.
        * Privileges required: **edit**
        """
        data = request.json
        val_num(id)
        val_alpha_num_special(data.get('name'))
        val_alpha_num_special(data.get('description'))
        validate_privilege(self, 'edit')
        result = update_sprint(id, data)
        return result, 200, security_headers()
