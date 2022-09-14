from flask_restx import Resource

from seckf.api.kb.parsers import authorization
from seckf.api.labs.business import deploy_labs
from seckf.api.labs.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, select_userid_jwt, validate_privilege

ns = api.namespace('interactive_labs', description='Operations related to the labs')


@api.expect(authorization)
@ns.route('/deployments/<int:instance_id>')
@api.response(404, 'Validation error', message)
class LabDeploy(Resource):

    # @api.marshal_with(lab_items)
    @api.response(400, 'No results found', message)
    def get(self, instance_id):
        """
        Returns list of labs.
        * Privileges required: **none**
        """
        userid = select_userid_jwt(self)
        validate_privilege(self, 'read')
        result = deploy_labs(instance_id, userid)
        return result, 200, security_headers()
