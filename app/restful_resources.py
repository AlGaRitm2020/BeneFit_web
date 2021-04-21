from flask import jsonify, request
from flask_login import current_user
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.user_inputs import UserInputs
from data.user_results import UserResults


def abort_if_inputs_not_found(user_id):
    """Response for incorrect user id"""
    session = db_session.create_session()
    user = session.query(UserInputs).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class InputsResource(Resource):

    def get(self, user_id):
        """this method return all of user inputs in json from database"""
        abort_if_inputs_not_found(user_id)
        session = db_session.create_session()
        user_inputs = session.query(UserInputs).get(user_id)
        user_results = session.query(UserResults).get(user_id)
        return jsonify({'user_inputs': user_inputs.to_dict(
            only=(
                'height', 'weight', 'age', 'gender', 'activity', 'wrists', 'waist', 'neck', 'hip'))})


class UpdateUser(Resource):
    """NOT USED NOW
    """

    def post(self):
        """this method post all of user inputs in database"""
        args = parser.parse_args()
        session = db_session.create_session()

        current_user.user_inputs[0].weight = args['weight']
        current_user.user_inputs[0].height = args['height']
        current_user.user_inputs[0].age = args['age']
        current_user.user_inputs[0].gender = args['gender']
        current_user.user_inputs[0].activity = args['activity']
        current_user.user_inputs[0].wrists = args['wrists']
        current_user.user_inputs[0].waist = args['waist']
        current_user.user_inputs[0].neck = args['neck']
        current_user.user_inputs[0].hip = args['hip']

        session.merge(current_user)
        session.commit()

        return jsonify({'success': 'OK'})


class ResultsResource(Resource):
    def get(self, **user_id):
        """this method return same user results(BMI, body type) in json from database"""
        abort_if_inputs_not_found(user_id)
        session = db_session.create_session()
        user_results = session.query(UserResults).get(user_id)
        return jsonify({'user_results': user_results.to_dict(
            only=(
                'BMI', 'body_type'))})


"""parser for UpdateUser class"""
parser = reqparse.RequestParser()
parser.add_argument('height', type=int)
parser.add_argument('weight', type=int)
parser.add_argument('age', type=int)
parser.add_argument('gender', type=bool)
parser.add_argument('activity', type=int)
parser.add_argument('wrists', type=int)
parser.add_argument('waist', type=int)
parser.add_argument('hip', type=int)
parser.add_argument('neck', type=int)
