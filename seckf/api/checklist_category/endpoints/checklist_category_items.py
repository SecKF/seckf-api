from flask_restx import Resource

from seckf.api.checklist_category.business import get_checklist_categories
from seckf.api.checklist_category.serializers import checklist_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers

ns = api.namespace('checklist_category', description='Operations related to checklist items')


@ns.route('/items')
@api.response(404, 'Validation error', message)
class ChecklistCategoryCollection(Resource):

    @api.marshal_with(checklist_items)
    @api.response(400, 'No results found', message)
    def get(self):
        """
        Returns list of checklist categories.
        * Privileges required: **none**
        """
        result = get_checklist_categories()
        return result, 200, security_headers()
