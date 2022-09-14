from flask_restx import Resource

from seckf.api.code.business import get_code_item
from seckf.api.code.serializers import code, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('code', description='Operations related to code example items')


@ns.route('/<int:id>')
@api.doc(params={'id': 'The code item id'})
@api.response(404, 'Validation error', message)
class CodeItem(Resource):

    @api.marshal_with(code)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns a code example item.
        * Privileges required: **none**
        """
        val_num(id)
        result = get_code_item(id)
        return result, 200, security_headers()
