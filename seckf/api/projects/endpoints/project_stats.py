from flask_restx import Resource

from seckf.api.projects.business import stats_project
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import message, project_stats
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('project', description='Operations related to project items')


@ns.route('/stats/<int:id>')
@api.doc(params={'id': 'The project id'})
@api.response(404, 'Validation error', message)
class ProjectStats(Resource):

    @api.expect(authorization)
    @api.marshal_with(project_stats)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns project stats.
        * Privileges required: **read**
        """
        val_num(id)
        validate_privilege(self, 'read')
        result = stats_project(id)
        return result, 200, security_headers()
