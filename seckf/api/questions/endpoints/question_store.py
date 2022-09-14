from flask import request
from flask_restx import Resource

from seckf.api.questions.business import store_questions
from seckf.api.questions.parsers import authorization
from seckf.api.questions.serializers import store_list_items, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege

ns = api.namespace('questions', description='Operations related to question items')


@ns.route('/store/<int:checklist_type>/<int:maturity>')
@api.response(404, 'Validation error', message)
class QuestionSprintStoreCollection(Resource):

    @api.expect(authorization, store_list_items)
    @api.marshal_with(message, 'Success')
    @api.response(400, 'No results found', message)
    def put(self, checklist_type, maturity):
        """
        Store list of question sprint items.
        * Privileges required: **edit**
        """
        validate_privilege(self, 'edit')
        data = request.json
        result = store_questions(checklist_type, maturity, data)
        return result, 200, security_headers()
