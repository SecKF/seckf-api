from flask import request
from flask_restx import Resource

from seckf.api.questions.business import new_question
from seckf.api.questions.parsers import authorization
from seckf.api.questions.serializers import question_item, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_alpha_num

ns = api.namespace('questions', description='Operations related to question sprint items')


@ns.route('/item/new')
@api.response(404, 'Validation error', message)
class QuestionSprintCollection(Resource):

    @api.expect(authorization, question_item)
    @api.response(400, 'No results found', message)
    def put(self):
        """
        Create new questions .
        * Privileges required: **edit**
        """
        data = request.json
        val_alpha_num(data.get('question'))
        validate_privilege(self, 'edit')
        result = new_question(data)
        return result, 200, security_headers()
