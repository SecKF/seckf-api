from flask_restx import Resource

from seckf.api.code.business import create_code_item_checklist_kb
from seckf.api.code.parsers import authorization
from seckf.api.code.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('code', description='Operations related to code example items')


@ns.route('/items/requirements/new/<int:checklist_kb_id>/<int:code_id>')
@api.response(404, 'Validation error', message)
class CodeCollection(Resource):

    @api.expect(authorization)
    # @api.marshal_with(code_items_checklist_kb_all)
    @api.response(400, 'No results found', message)
    def put(self, checklist_kb_id, code_id):
        """
        Correlate code example item to requirements
        * Privileges required: **edit**
        """
        val_num(checklist_kb_id)
        val_num(code_id)
        validate_privilege(self, 'edit')
        result = create_code_item_checklist_kb(checklist_kb_id, code_id)
        return result, 200, security_headers()
