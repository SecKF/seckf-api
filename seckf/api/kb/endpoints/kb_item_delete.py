from flask_restx import Resource

from seckf.api.kb.business import delete_kb_item
from seckf.api.kb.parsers import authorization
from seckf.api.kb.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('kb', description='Operations related to knowledge base')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The project id'})
@api.response(404, 'Validation error', message)
class KnowledgebaseItemDelete(Resource):

    @api.expect(authorization)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Deletes project item.
        * Privileges required: **delete**
        """
        validate_privilege(self, 'delete')
        val_num(id)
        result = delete_kb_item(id)
        return result, 200, security_headers()
