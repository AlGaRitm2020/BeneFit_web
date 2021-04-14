import os

from app__ import *
from waitress import serve

from BeneFit_web.app import restful_resources
from BeneFit_web.app__ import api, app
from BeneFit_web.data import db_session

if __name__ == '__main__':
    db_session.global_init("db/users.db")
    port = int(os.environ.get("PORT", 8080))
    # app.run(host='0.0.0.0', port=port)
    api.add_resource(restful_resources.InputsResource, '/api/user/<int:user_id>/inputs')
    api.add_resource(restful_resources.ResultsResource, '/api/user/<int:user_id>/results')

    api.add_resource(restful_resources.UpdateUser, '/api/user')
    # api.add_resource(restful_resources.I, '/api/user_inputs/<int:user_id>')
    serve(app, host='0.0.0.0', port=port)