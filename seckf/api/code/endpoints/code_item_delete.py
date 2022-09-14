from flask_restx import Resource

from seckf.api.code.business import delete_code_item
from seckf.api.code.parsers import authorization
from seckf.api.code.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege

ns = api.namespace('code', description='Operations related to knowledge base')


@ns.route('/delete/<int:id>')
@api.doc(params={'id': 'The code id'})
@api.response(404, 'Validation error', message)
class KnowledgebaseItemDelete(Resource):

    @api.expect(authorization)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def delete(self, id):
        """
        Deletes code item.
        * Privileges required: **delete**
        """
        validate_privilege(self, 'delete')
        result = delete_code_item(id)
        return result, 200, security_headers()
