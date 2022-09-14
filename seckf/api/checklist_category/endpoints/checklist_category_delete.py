from flask_restx import Resource

from seckf.api.checklist_category.business import delete_checklist_category
from seckf.api.checklist_category.serializers import message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('checklist_category', description='Operations related to checklist items')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The checklist type id'})
@api.response(404, 'Validation error', message)
class ChecklistCategoryDelete(Resource):

    @api.expect(authorization)
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Delete a checklist type.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_checklist_category(id)
        return result, 200, security_headers()
