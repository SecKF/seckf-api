from flask_restx import Resource

from seckf.api.checklist.business import get_checklist_item
from seckf.api.checklist.serializers import checklist_item, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/item/<int:id>')
@api.doc(params={'id': 'The ID of the checklist item'})
@api.response(404, 'Validation error', message)
class ChecklistItem(Resource):

    @api.marshal_with(checklist_item)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns a single checklist item.
        * Privileges required: **none**
        """
        val_num(id)
        result = get_checklist_item(id)
        return result, 200, security_headers()
