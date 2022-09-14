from flask_restx import Resource

from seckf.api.labs.serializers import lab_items_solutions, message
from seckf.api.labs_code.business import get_labs_code_sol
from seckf.api.restplus import api
from seckf.api.security import security_headers, val_num

ns = api.namespace('interactive_labs', description='Operations related to the labs')


@ns.route('/code/items/solutions/<int:solutions_id>')
@api.doc(params={'solutions_id': 'The code solutions items'})
@api.response(404, 'Validation error', message)
class LabCollectionCodeSolutions(Resource):
    @api.marshal_with(lab_items_solutions)
    @api.response(400, 'No results found', message)
    def get(self, solutions_id):
        """
        Returns list of code solutions for the review labs.
        * Privileges required: **none**
        """
        val_num(solutions_id)
        result = get_labs_code_sol(solutions_id)
        return result, 200, security_headers()
