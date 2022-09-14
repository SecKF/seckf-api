from flask import request
from flask_restx import Resource

from seckf.api.checklist.business import update_checklist_item
from seckf.api.checklist.serializers import checklist_create_update, message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha_num, val_alpha_num_special

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/update/item/<int:id>')
@api.doc(params={'id': 'The checklist item db ID '})
@api.response(404, 'Validation error', message)
class ChecklistItemUpdate(Resource):

    @api.expect(authorization, checklist_create_update)
    @api.response(400, 'No results found', message)
    def put(self, id):
        """
        Update a checklist item.
        * Privileges required: **edit**
        """
        data = request.json
        val_num(id)
        val_num(data.get('maturity'))
        val_num(data.get('question_id'))
        val_alpha_num_special(data.get('add_resources'))
        val_num(data.get('kb_id'))
        val_alpha_num(data.get('include_always'))
        val_alpha_num_special(data.get('content'))
        validate_privilege(self, 'edit')
        result = update_checklist_item(id, data)
        return result, 200, security_headers()
