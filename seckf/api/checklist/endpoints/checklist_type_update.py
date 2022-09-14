from flask import request
from flask_restx import Resource

from seckf.api.checklist.business import update_checklist_type
from seckf.api.checklist.serializers import checklist_type, message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege, val_num, val_alpha_num_special

ns = api.namespace('checklist_types', description='Operations related to checklist types')


@ns.route('/update/<int:id>')
@api.doc(params={'id': 'The checklist type id'})
@api.response(404, 'Validation error', message)
class ChecklistUpdate(Resource):

    @api.expect(authorization, checklist_type)
    @api.response(400, 'No results found', message)
    def put(self, id):
        """
        Update a checklist type.
        * Privileges required: **edit**
        """
        data = request.json
        val_num(id)
        val_alpha_num_special(data.get('name'))
        val_alpha_num_special(data.get('description'))
        validate_privilege(self, 'edit')
        result = update_checklist_type(id, data)
        return result, 200, security_headers()
