from flask_restx import Resource

from seckf.api.checklist_category.business import get_checklist_category_item
from seckf.api.checklist_category.serializers import checklist_type, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('checklist_category', description='Operations related to checklist items')


@ns.route('/<int:id>')
@api.doc(params={'id': 'The category'})
@api.response(404, 'Validation error', message)
class ChecklistCategoryCollection(Resource):

    @api.marshal_with(checklist_type)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns a single checklist category.
        * Privileges required: **none**
        """
        val_num(id)
        result = get_checklist_category_item(id)
        return result, 200, security_headers()
