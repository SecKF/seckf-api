from flask_restx import Resource

from seckf.api.projects.business import get_project_items
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import page_of_project_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege

ns = api.namespace('project', description='Operations related to project items')


@ns.route('/items')
@api.response(404, 'Validation error', message)
class ProjectCollection(Resource):

    @api.expect(authorization)
    @api.marshal_with(page_of_project_items)
    @api.response(400, 'No results found', message)
    def get(self):
        """
        Returns list of project items.
        * Privileges required: **read**
        """
        validate_privilege(self, 'read')
        result = get_project_items()
        return result, 200, security_headers()
