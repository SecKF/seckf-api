from flask_restx import Resource

from seckf.api.kb.business import get_kb_item
from seckf.api.kb.serializers import kb, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('kb', description='Operations related to kb items')


@ns.route('/<int:id>')
@api.doc(params={'id': 'The kb item id'})
@api.response(404, 'Validation error', message)
class KBItem(Resource):

    @api.marshal_with(kb)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns a kb item.
        * Privileges required: **none**
        """
        val_num(id)
        result = get_kb_item(id)
        return result, 200, security_headers()
