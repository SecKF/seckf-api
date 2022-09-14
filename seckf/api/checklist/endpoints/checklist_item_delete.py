from flask_restx import Resource

from seckf.api.checklist.business import delete_checklist_item
from seckf.api.checklist.serializers import message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/delete/item/<int:id>')
@api.doc(params={'id': 'DB id of the checklist item'})
@api.response(404, 'Validation error', message)
class ChecklistItemDelete(Resource):

    @api.expect(authorization)
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Delete a checklist item.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_checklist_item(id)
        return result, 200, security_headers()
