from flask import request
from flask_restx import Resource

from seckf.api.questions.business import update_question
from seckf.api.questions.parsers import authorization
from seckf.api.questions.serializers import question_item, message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege

ns = api.namespace('questions', description='Operations related to questions')


@ns.route('/item/update/<int:id>')
@api.doc(params={'id': 'The unique question id'})
@api.response(404, 'Validation error', message)
class QuestionSprintCollection(Resource):

    @api.expect(authorization, question_item)
    @api.response(404, 'No results found', message)
    def put(self, id):
        """
        Update question sprint item.
        * Privileges required: **edit**
        """
        validate_privilege(self, 'edit')
        data = request.json
        result = update_question(id, data)
        return result, 200, security_headers()
