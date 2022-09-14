from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num
from seckf.api.sprints.business import stats_sprint
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import message, sprint_stats

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/stats/<int:id>')
@api.doc(params={'id': 'The project id'})
@api.response(404, 'Validation error', message)
class ProjectSprintStats(Resource):

    @api.expect(authorization)
    @api.marshal_with(sprint_stats)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns sprints stats.
        * Privileges required: **read**
        """
        val_num(id)
        validate_privilege(self, 'read')
        result = stats_sprint(id)
        return result, 200, security_headers()
