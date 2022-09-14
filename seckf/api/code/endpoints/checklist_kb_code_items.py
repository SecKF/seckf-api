from flask_restx import Resource

from seckf.api.code.business import get_code_items_checklist_kb
from seckf.api.code.parsers import authorization
from seckf.api.code.serializers import code_items_checklist_kb_all, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_alpha_num_special

ns = api.namespace('code', description='Operations related to code example items')


@ns.route('/items/requirements/<int:checklist_kb_id>')
@api.response(404, 'Validation error', message)
class CodeCollection(Resource):

    @api.expect(authorization)
    @api.marshal_with(code_items_checklist_kb_all)
    @api.response(400, 'No results found', message)
    def get(self, checklist_kb_id):
        """
        Returns list of code example items that have correlation with requirements.
        * Privileges required: **edit**
        """
        val_alpha_num_special(checklist_kb_id)
        validate_privilege(self, 'edit')
        result = get_code_items_checklist_kb(checklist_kb_id)
        return result, 200, security_headers()
