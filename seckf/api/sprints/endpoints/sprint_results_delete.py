from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.sprints.business import delete_checklist_result
from seckf.api.sprints.parsers import authorization
from seckf.api.sprints.serializers import delete_checklist_results, message

ns = api.namespace('sprint', description='Operations related to sprint items')


@ns.route('/results/delete/<int:checklist_result_id>')
@api.doc(params={'id': 'checklist_results_id'})
@api.response(404, 'Validation error', message)
class ProjectSprintResultItemDelete(Resource):

    @api.expect(authorization)
    @api.marshal_with(delete_checklist_results)
    @api.response(400, 'No results found', message)
    def delete(self, checklist_result_id):
        """
        Deletes a checklist_result item from your sprint/feature.
        * Privileges required: **read**
        """
        validate_privilege(self, 'read')
        result = delete_checklist_result(checklist_result_id)
        return result, 200, security_headers()
