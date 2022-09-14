from flask_restx import Resource

from seckf.api.kb.business import get_kb_items
from seckf.api.kb.serializers import kb_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('kb', description='Operations related to kb items')


@ns.route('/items/<int:category_id>')
@api.response(404, 'Validation error', message)
class KBCollection(Resource):

    @api.marshal_with(kb_items)
    @api.response(400, 'No results found', message)
    def get(self, category_id):
        """
        Returns list of kb items.
        * Privileges required: **none**
        """
        val_num(category_id)
        result = get_kb_items(category_id)
        return result, 200, security_headers()
