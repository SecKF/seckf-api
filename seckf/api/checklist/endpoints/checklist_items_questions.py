from flask_restx import Resource

from seckf.api.checklist.business import get_checklist_item_questions_git
from seckf.api.checklist.serializers import checklist_items_questions, message
from seckf.api.restplus import api
from seckf.api.security import security_headers
from seckf.api.security import val_num

ns = api.namespace('checklist', description='Operations related to checklist items')


@ns.route('/item/gitplugin/<int:checklist_type>')
@api.response(404, 'Validation error', message)
class ChecklistItemQuestions(Resource):

    @api.marshal_with(checklist_items_questions)
    @api.response(400, 'No results found', message)
    def get(self, checklist_type):
        """
        Returns a list of checklist items, questions, knowledgebase items correlated to a checklist type
        * Privileges required: **none**
        """
        val_num(checklist_type)
        result = get_checklist_item_questions_git(checklist_type)
        return result, 200, security_headers()
