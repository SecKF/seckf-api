from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.sprints.business import get_sprint_results
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import sprint_results, message

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/results/<int:id>')
@api.doc(params={'id': 'The sprint id'})
@api.response(404, 'Validation error', message)
class ProjectSprintResultItem(Resource):

    @api.expect(authorization)
    @api.marshal_with(sprint_results)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns sprint items.
        * Privileges required: **read**
        """
        validate_privilege(self, 'read')
        result = get_sprint_results(id)
        return result, 200, security_headers()
