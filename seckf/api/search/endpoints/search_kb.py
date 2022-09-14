from flask_restx import Resource

from seckf.api.restplus import api
from seckf.api.search.business import search_kb
from seckf.api.search.parsers import authorization
from seckf.api.search.serializers import kb, message
from seckf.api.security import security_headers, validate_privilege

ns = api.namespace('search', description='Operations related to the search functionality')


@ns.route('/kb/<string:search_string>')
@api.response(404, 'Validation error', message)
class SearchKb(Resource):

    @api.expect(authorization)
    @api.marshal_with(kb)
    @api.response(400, 'No results found', message)
    def get(self, search_string):
        """
        Returns list of search kb hits.
        * Privileges required: **read**
        """
        validate_privilege(self, 'read')
        result = search_kb(search_string)
        return result, 200, security_headers()
