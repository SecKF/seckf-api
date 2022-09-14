from flask_restx import Resource

from seckf.api.checklist.business import delete_checklist_type
from seckf.api.checklist.serializers import message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('checklist_types', description='Operations related to checklist types')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The checklist type id'})
@api.response(404, 'Validation error', message)
class ChecklistDelete(Resource):

    @api.expect(authorization)
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Delete a checklist type.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_checklist_type(id)
        return result, 200, security_headers()
