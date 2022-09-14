from flask_restx import Resource

from seckf.api.checklist.business import get_checklist_type_by_id
from seckf.api.checklist.serializers import checklist_type, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('checklist_types', description='Operations related to checklist types')


@ns.route('/type/<int:checklist_type_id>')
@api.response(404, 'Validation error', message)
class ChecklistCollection(Resource):

    @api.marshal_with(checklist_type)
    @api.response(400, 'No results found', message)
    def get(self, checklist_type_id):
        """
        Returns a single checklist types content by the checklist type id
        * Privileges required: **none**
        """
        val_num(checklist_type_id)
        result = get_checklist_type_by_id(checklist_type_id)
        return result, 200, security_headers()
