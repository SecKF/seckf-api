from flask_restx import Resource

from seckf.api.labs_code.business import verify_user_answer
from seckf.api.labs_code.parsers import authorization
from seckf.api.labs_code.serializers import labs_code_status, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, val_num, select_userid_jwt

ns = api.namespace('code_review_labs', description='Operations related to the labs')


@ns.route('/solve_challenge/<int:code_id>/solution/<int:solution_id>')
@api.doc(params={'code_id': 'The unique id of the code item', 'solution_id': 'The unique id of the code item solution'})
@api.response(404, 'Validation error', message)
class LabCollectionCodeStatus(Resource):

    @api.expect(authorization)
    @api.marshal_with(labs_code_status)
    @api.response(400, 'No results found', message)
    def get(self, code_id, solution_id):
        """
        Returns status if solution was correct for code item.
        * Privileges required: **none**
        """
        val_num(code_id)
        val_num(solution_id)
        user_id = select_userid_jwt(self)
        result = verify_user_answer(user_id, code_id, solution_id)
        return result, 200, security_headers()
