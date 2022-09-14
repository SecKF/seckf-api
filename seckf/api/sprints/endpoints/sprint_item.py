from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num
from seckf.api.sprints.business import get_sprint_item
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import sprint, message

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/<int:id>')
@api.doc(params={'id': 'The sprint id'})
@api.response(404, 'Validation error', message)
class ProjectSprintItem(Resource):

    @api.expect(authorization)
    @api.marshal_with(sprint)
    @api.response(400, 'No results found', message)
    def get(self, id):
        """
        Returns a sprint item.
        * Privileges required: **read**
        """
        val_num(id)
        validate_privilege(self, 'read')
        result = get_sprint_item(id)
        return result, 200, security_headers()
