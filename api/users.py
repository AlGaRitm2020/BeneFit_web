"""NOT USED NOW"""

from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('password_again', required=True)
parser.add_argument('name', required=True)


class RegisterRes(Resource):
    def post(self):
        args = parser.parse_args()
        # check password match
        if args['password'] != args['password_again']:
            # passwords isn't match
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   bg_index=bg_index)
        # new session
        db_sess = db_session.create_session()

        # check registered
        if db_sess.query(UserLogin).filter(UserLogin.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   bg_index=bg_index)
        # user login info
        user_login = UserLogin(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )

        user_login.set_password(form.password.data)
        db_sess.add(user_login)

        user_inputs = UserInputs(
            weight=70,
            height=175,
            age=25,
            gender="Мужской",
            activity=2,
            wrists=18,
            waist=70,
            neck=40,
            hip=80
        )

        user_results = UserResults(
            BMI=22,
            body_type='Мезоморф'
        )

        user_login.user_inputs.append(user_inputs)
        db_sess.merge(user_login)
        db_sess.commit()

        user_login.user_results.append(user_results)
        db_sess.merge(user_login)
        db_sess.commit()

        return redirect('/login')

