from flask import jsonify, request
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


class ResultsResource(Resource):
    def get(self, user_id):
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
# parser = reqparse.RequestParser()
# parser.add_argument('title', required=True)
# parser.add_argument('content', required=True)
# parser.add_argument('is_private', required=True, type=bool)
# parser.add_argument('is_published', required=True, type=bool)
# parser.add_argument('user_id', required=True, type=int)
