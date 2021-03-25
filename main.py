# flask framework
from flask import Flask, render_template, request, make_response, session, redirect, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_restful import reqparse, abort, Api, Resource
# models
from data import db_session, restful_resourses
from data.user_inputs import User_inputs
from data.user_login import User_login

# forms
from forms.BMI_calculator_form import BMICalculatorForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm

# extra modules
import datetime

# flask init
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# login manager init
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """"Get user with user_id"""
    db_sess = db_session.create_session()
    return db_sess.query(User_login).get(user_id)


@app.route("/")
def home_page():
    """"Home page (/) show all current user news and all public news"""
    return render_template("index.html")


@app.route("/calculators", methods=['GET', "POST"])
def calculators_page():
    """Show all calculators"""
    return render_template("calculators.html", title='Калькулятор')


@app.route("/calculators/BMI", methods=['GET', "POST"])
def calculator_BMI_page():
    """"BMI Calculator page
    using weight and height"""

    form = BMICalculatorForm()

    if form.validate_on_submit():
        """Submit pressed"""
        weight = form.weight.data
        height = form.height.data
        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].weight = weight
            current_user.user_inputs[0].height = height
            db_sess.merge(current_user)
            db_sess.commit()
            # anonymous

        BMI = round(weight / (height / 100) ** 2, 1)
        return render_template("BMI_calculator.html", title='Калькулятор индекса массы тела', form=form, BMI=BMI)

    if current_user.is_authenticated:
        """Get user_inputs from database and insert into form"""
        db_sess = db_session.create_session()
        current_user_inputs = db_sess.query(User_inputs).filter(User_inputs.user_id == current_user.id).first()

        form.height.data = current_user_inputs.height
        form.weight.data = current_user_inputs.weight

    return render_template("BMI_calculator.html", title='Калькулятор индекса массы тела', form=form)


@app.route('/calculators/BMI/results')
def calculator_results_page(**json):
    weight = current_user.user_inputs[0].weight
    height = current_user.user_inputs[0].height
    BMI = round(weight / (height / 100) ** 2, 1)
    return render_template('calculator_results.html', title='Регистрация', BMI=BMI)


@app.route('/register', methods=['GET', 'POST'])
def reqister_page():
    """"Register user with Register Form
    Fields: name, email, about, password"""
    form = RegisterForm()
    # register button
    if form.validate_on_submit():
        # check password match
        if form.password.data != form.password_again.data:
            # passwords isn't match
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # new session
        db_sess = db_session.create_session()
        # check registered
        if db_sess.query(User_login).filter(User_login.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        # user login info
        user_login = User_login(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )

        user_login.set_password(form.password.data)
        db_sess.add(user_login)

        user_data = User_inputs(
            weight=0,
            height=0
        )

        user_login.user_inputs.append(user_data)
        db_sess.merge(user_login)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """"Login using email and password
    Check correctness login and password
    After that, redirect to home(/) """
    # login form
    form = LoginForm()

    # submit button
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # user search
        user = db_sess.query(User_login).filter(User_login.email == form.email.data).first()
        # check password
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # go home
            return redirect("/")

        # user error
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    # return template
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout_page():
    """"Logout page
    kill current user session and redirect to home(/)"""
    logout_user()
    return redirect("/")


def main():
    """"Initilize database session and run application"""
    db_session.global_init("db/users.db")

    # для одного объекта
    api.add_resource(restful_resourses.InputsResource, '/api/user_inputs/<int:user_id>')

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
