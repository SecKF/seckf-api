from flask_restx import Resource

from seckf.api.labs.business import get_labs
from seckf.api.labs.serializers import lab_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers

ns = api.namespace('interactive_labs', description='Operations related to the labs')


@ns.route('/items')
@api.response(404, 'Validation error', message)
class LabCollection(Resource):
    @api.marshal_with(lab_items)
    @api.response(400, 'No results found', message)
    def get(self):
        """
        Returns list of labs.
        * Privileges required: **none**
        """
        result = get_labs()
        return result, 200, security_headers()
