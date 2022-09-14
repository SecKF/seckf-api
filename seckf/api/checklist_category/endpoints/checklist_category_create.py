from flask import request
from flask_restx import Resource

from seckf.api.checklist_category.business import create_checklist_category
from seckf.api.checklist_category.serializers import checklist_type, message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_alpha_num_special

ns = api.namespace('checklist_category', description='Operations related to checklist category')


@ns.route('/new')
@api.response(404, 'Validation error', message)
class ChecklistCategoryCreate(Resource):

    @api.expect(authorization, checklist_type)
    @api.response(400, 'No results found', message)
    def put(self):
        """
        Create a new checklist category.
        * Privileges required: **edit**
        """
        data = request.json
        val_alpha_num_special(data.get('name'))
        val_alpha_num_special(data.get('description'))
        validate_privilege(self, 'edit')
        result = create_checklist_category(data)
        return result, 200, security_headers()
