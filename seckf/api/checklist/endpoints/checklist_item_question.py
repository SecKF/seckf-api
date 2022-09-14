from flask_restx import Resource

from seckf.api.checklist.business import get_checklist_item_question_sprint
from seckf.api.checklist.serializers import checklist_items, message
from seckf.api.kb.parsers import authorization
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/item/question_sprint/<int:question_id>')
@api.doc(params={'questionID': 'The checklist item questionID'})
@api.response(404, 'Validation error', message)
class ChecklistItemQuestion(Resource):

    @api.expect(authorization)
    @api.marshal_with(checklist_items)
    @api.response(400, 'No results found', message)
    def get(self, question_id):
        """
        Returns a list of checklist items correlated to question sprint identifier
        * Privileges required: **read**
        """
        val_num(question_id)
        validate_privilege(self, 'read')
        result = get_checklist_item_question_sprint(question_id)
        return result, 200, security_headers()
