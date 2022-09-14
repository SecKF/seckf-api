from flask import request
from flask_restx import Resource

from seckf.api.code.business import update_code_item
from seckf.api.code.parsers import authorization
from seckf.api.code.serializers import code_properties, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num, val_alpha_num_special

ns = api.namespace('code', description='Operations related to code example items')


@ns.route('/update/<int:id>')
@api.doc(params={'id': 'The code item id'})
@api.response(404, 'Validation error', message)
class CodeItemUpdate(Resource):

    @api.expect(authorization, code_properties)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'Validation Error', message)
    def put(self, id):
        """
        Update a code example item.
        * Privileges required: **edit**
        """
        data = request.json
        val_alpha_num_special(data.get('title'))
        val_num(id)
        validate_privilege(self, 'edit')
        result = update_code_item(id, data)
        return result, 200, security_headers()
