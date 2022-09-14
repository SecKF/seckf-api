from flask import request
from flask_restx import Resource

from seckf.api.kb.business import create_kb_item
from seckf.api.kb.parsers import authorization
from seckf.api.kb.serializers import kb_update, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_alpha_num_special

ns = api.namespace('kb', description='Operations related to kb items')


@ns.route('/new/<int:category_id>')
@api.response(404, 'Validation error', message)
class KBItemCreate(Resource):

    @api.expect(authorization, kb_update)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, category_id):
        """
        Create new kb item.
        * Privileges required: **edit**
        """
        validate_privilege(self, 'edit')
        data = request.json
        val_alpha_num_special(data.get('title'))
        result = create_kb_item(data, category_id)
        return result, 200, security_headers()
