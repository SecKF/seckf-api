from flask_restx import Resource

from seckf.api.checklist.business import update_checklist_question_correlation
from seckf.api.checklist.serializers import message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/update/item/correlation/<int:id>/question/<int:question_id>')
@api.doc(params={'id': 'The checklist item id'})
@api.response(404, 'Validation error', message)
class ChecklistQuestionCorrelationUpdate(Resource):

    @api.expect(authorization)
    @api.response(400, 'No results found', message)
    def get(self, id, question_id):
        """
        Update a checklist item correlated to question
        * Privileges required: **edit**
        """
        val_num(id)
        val_num(question_id)
        validate_privilege(self, 'edit')
        result = update_checklist_question_correlation(id, question_id)
        return result, 200, security_headers()
