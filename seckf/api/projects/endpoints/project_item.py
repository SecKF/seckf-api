from flask_restx import Resource

from seckf.api.projects.business import get_project_item
from seckf.api.projects.parsers import authorization
from seckf.api.projects.serializers import project_update, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('project', description='Operations related to kb items')


@ns.route('/item/<int:id>')
@api.doc(params={'id': 'The project item id'})
@api.response(404, 'Validation error', message)
class Project(Resource):

    @api.expect(authorization, get_project_item)
    @api.marshal_with(project_update)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Create new project item.
        * Privileges required: **edit**
        """
        val_num(id)
        result = get_project_item(id)
        validate_privilege(self, 'edit')
        return result, 200, security_headers()
