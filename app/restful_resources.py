from flask import jsonify, request
from flask_login import current_user
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.user_inputs import UserInputs
from data.user_results import UserResults


def abort_if_inputs_not_found(news_id):
    session = db_session.create_session()
    news = session.query(UserInputs).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class InputsResource(Resource):

    def get(self, user_id):
        abort_if_inputs_not_found(user_id)
        session = db_session.create_session()
        user_inputs = session.query(UserInputs).get(user_id)
        user_results = session.query(UserResults).get(user_id)
        return jsonify({'user_inputs': user_inputs.to_dict(
            only=(
                'height', 'weight', 'age', 'gender', 'activity', 'wrists', 'waist', 'neck', 'hip'))})


class UpdateUser(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        # inputs = UserInputs(
        #     height=args['height'],
        #     weight=args['weight'],
        #     age=args['age'],
        #     gender=args['gender'],
        #     activity=args['activity'],
        #     wrists=args['wrists'],
        #     waist=args['waist'],
        #     neck=args['neck'],
        #     hip=args['hip']
        # )

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
        abort_if_inputs_not_found(user_id)
        session = db_session.create_session()
        user_results = session.query(UserResults).get(user_id)
        return jsonify({'user_inputs': user_results.to_dict(
            only=(
                'BMI', 'body_type'))})

    # def delete(self, user_id):
    #     abort_if_inputs_not_found(user_id)
    #     session = db_session.create_session()
    #     user_inputs = session.query(UserInputs).get(user_id)
    #     session.delete(user_inputs)
    #     session.commit()
    #     return jsonify({'success': 'OK'})


# class InputsListResource(Resource):
#     def get(self):
#         session = db_session.create_session()
#         news = session.query(UserInputs).all()
#         return jsonify({'news': [item.to_dict(
#             only=('title', 'content', 'user.name')) for item in news]})
#
#     def post(self):
#         args = parser.parse_args()
#         session = db_session.create_session()
#         news = News(
#             title=args['title'],
#             content=args['content'],
#             user_id=args['user_id'],
#             is_published=args['is_published'],
#             is_private=args['is_private']
#         )
#         session.add(news)
#         session.commit()
#         return jsonify({'success': 'OK'})
#
#
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
