from flask import request
from flask_restx import Resource

from seckf.api.kb.business import update_kb_item
from seckf.api.kb.parsers import authorization
from seckf.api.kb.serializers import kb_update, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha_num_special

ns = api.namespace('kb', description='Operations related to kb items')


@ns.route('/update/<int:kb_id>')
@api.doc(params={'id': 'The kb item id'})
@api.response(404, 'Validation error', message)
class KBItemUpdate(Resource):

    @api.expect(authorization, kb_update)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, kb_id):
        """
        Update a kb item.
        * Privileges required: **edit**
        """
        data = request.json
        val_num(kb_id)
        val_alpha_num_special(data.get('title'))
        validate_privilege(self, 'edit')
        result = update_kb_item(kb_id, data)
        return result, 200, security_headers()
