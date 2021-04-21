"""NOT USED NOW"""

from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('name', required=True)


class RegisterRes(Resource):
    def post(self):
        args = parser.parse_args()

