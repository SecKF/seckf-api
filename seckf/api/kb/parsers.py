from flask_restx import reqparse

authorization = reqparse.RequestParser()
authorization.add_argument('Authorization', location='headers', required=True, help='Authorization JWT token')
