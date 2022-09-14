from flask import request
from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num, val_alpha_num_special
from seckf.api.user.business import activate_user
from seckf.api.user.serializers import activate, message

ns = api.namespace('user', description='Operations related to users')


@ns.route('/activate/<int:id>')
@api.doc(params={'id': 'The user id'})
@api.response(404, 'Validation error', message)
class userActivation(Resource):

    @api.expect(activate)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, id):
        data = request.json
        val_num(data.get('accessToken'))
        val_alpha_num_special(data.get('username'))
        val_num(id)
        result = activate_user(id, data)
        return result, 200, security_headers()
