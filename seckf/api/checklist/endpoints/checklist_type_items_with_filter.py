from flask_restx import Resource

from seckf.api.checklist.business import get_checklist_item_types_with_filter
from seckf.api.checklist.serializers import checklist_type_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('checklist_types', description='Operations related to checklist types')


@ns.route('/by_maturity/<int:maturity>')
@api.doc(params={'maturity': 'The checklist type naturity level'})
@api.response(404, 'Validation error', message)
class ChecklistCollection(Resource):

    @api.marshal_with(checklist_type_items)
    @api.response(400, 'No results found', message)
    def get(self, maturity):
        """
        Returns list of checklist types.
        * Privileges required: **none**
        """
        val_num(maturity)
        result = get_checklist_item_types_with_filter(maturity)
        return result, 200, security_headers()
