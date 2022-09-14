from flask_restx import Resource

from seckf.api.questions.business import delete_question
from seckf.api.questions.parsers import authorization
from seckf.api.questions.serializers import message
from seckf.api.restplus import api
from seckf.api.security import security_headers, validate_privilege
from seckf.api.security import val_num

ns = api.namespace('questions', description='Operations related to questions')


@ns.route('/item/delete/<int:id>')
@api.doc(params={'id': 'The unique question id'})
@api.response(404, 'Validation error', message)
class QuestionSprintDelete(Resource):

    @api.expect(authorization)
    @api.response(404, 'No results found', message)
    def delete(self, id):
        """
        Delete questions.
        * Privileges required: **delete**
        """
        val_num(id)
        validate_privilege(self, 'delete')
        result = delete_question(id)
        return result, 200, security_headers()
