from flask_restx import Resource

from seckf.api.code.business import get_code_items
from seckf.api.code.serializers import code_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_alpha_num_special

ns = api.namespace('code', description='Operations related to code example items')


@ns.route('/items/<int:category_id>')
@api.response(404, 'Validation error', message)
class CodeCollection(Resource):

    @api.marshal_with(code_items)
    @api.response(400, 'No results found', message)
    def get(self, category_id):
        """
        Returns list of code example items.
        * Privileges required: **none**
        """
        val_alpha_num_special(category_id)
        result = get_code_items(category_id)
        return result, 200, security_headers()
