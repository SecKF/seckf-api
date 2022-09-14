from flask_restx import Resource

from seckf.api.labs_code.business import get_random_code_lab
from seckf.api.labs_code.parsers import authorization
from seckf.api.labs_code.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, val_alpha_num_special, select_userid_jwt

ns = api.namespace('code_review_labs', description='Operations related to the labs')


@ns.route('/challenge/<string:code_type>')
@api.doc(params={'code_type': 'The code type items based on name for example: php, asp, java'})
@api.response(404, 'Validation error', message)
class LabCollectionCode(Resource):

    @api.expect(authorization)
    # @api.marshal_with(labs_code)
    @api.response(400, 'No results found', message)
    def get(self, code_type):
        """
        Returns list of code review labs.
        * Privileges required: **none**
        """
        val_alpha_num_special(code_type)
        user_id = select_userid_jwt(self)
        result = get_random_code_lab(user_id, code_type.lower())
        return result, 200, security_headers()
