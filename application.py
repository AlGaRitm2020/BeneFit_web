# flask framework
import os
from random import randint

from waitress import serve
import requests

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_restful import Api
# models
from data import db_session
from app import restful_resources
from data.calculate import calculate_BMI, calculate_max_heart_rate, \
    calculate_training_heart_rate_min, calculate_training_heart_rate_max, calculate_water, \
    calculate_physical_activity_quotient, calculate_calories, calculate_body_type, \
    calculate_body_fat_percent
from app.restful_resources import ResultsResource
from data.user_inputs import UserInputs
from data.user_login import UserLogin
from data.user_results import UserResults

# forms
from forms.BMI_calculator_form import BMICalculatorForm
from forms.body_fat_calculator_form import BodyFatCalculatorForm
from forms.body_type_calculator_form import BodyTypeCalculatorForm
from forms.calorie_calculator_form import CalorieCalculatorForm
from forms.heart_rate_calculator_form import HeartRateCalculatorForm
from forms.profile_form import ProfileForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.water_calculator_form import WaterCalculatorForm
from forms.nutrition_search_form import NutritionSearchForm

# extra modules
import csv

# flask init

DOMAIN = 'http://benefit2021.herokuapp.com'
LOCAL_HOST = 'http://127.0.0.1:8080'


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
    return db_sess.query(UserLogin).get(user_id)


@app.route("/")
def home_page():
    """"Home page (/) show all current user news and all public news"""
    return render_template("index.html", active_home='active')


'''Pages
active_{pagename} attribute mean that this tab is active and send to template class 'active'
 in order to highlight this tab'''


@app.route("/calculators/BMI", methods=['GET', "POST"])
def BMI_calculator_page():
    """"BMI Calculator page
    using weight and height"""

    form = BMICalculatorForm()

    if form.validate_on_submit():
        """Submit pressed"""
        weight = form.weight.data
        height = form.height.data
        if current_user.is_authenticated:
            """user was authenticated
            save inputs to the database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].weight = weight
            current_user.user_inputs[0].height = height
            db_sess.merge(current_user)
            db_sess.commit()
            """save results to the database"""
            current_user.user_results[0].BMI = calculate_BMI(weight, height)
            db_sess.merge(current_user)
            db_sess.commit()

        BMI = calculate_BMI(weight, height)
        return render_template("BMI_calculator.html", title='?????????????????????? ?????????????? ?????????? ????????',
                               form=form, BMI=BMI, active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from api and insert into form"""

        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()

        form.height.data = inputs_json['user_inputs']['height']
        form.weight.data = inputs_json['user_inputs']['weight']

    return render_template("BMI_calculator.html", title='?????????????????????? ?????????????? ?????????? ????????',
                           form=form, active_calculator='active')


@app.route("/calculators/heart_rate", methods=['GET', "POST"])
def heart_rate_calculator_page():
    """"Heart Rate Calculator page
    using age"""

    form = HeartRateCalculatorForm()

    if form.validate_on_submit():
        """Submit pressed"""
        age = form.age.data
        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].age = age

            db_sess.merge(current_user)
            db_sess.commit()

        max_heart_rate = calculate_max_heart_rate(age)
        training_heart_rate_min = calculate_training_heart_rate_min(age)
        training_heart_rate_max = calculate_training_heart_rate_max(age)
        return render_template("heart_rate_calculator.html",
                               title='?????????????????????? ?????????????? ?????????????????? ????????????????????', form=form,
                               MHR=max_heart_rate, THR_min=training_heart_rate_min,
                               THR_max=training_heart_rate_max,
                               active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from api and insert into form"""
        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()
        form.age.data = inputs_json['user_inputs']['age']

    return render_template("heart_rate_calculator.html",
                           title='?????????????????????? ?????????????? ?????????????????? ????????????????????', form=form,
                           active_calculator='active')


@app.route("/calculators/water", methods=['GET', "POST"])
def water_calculator_page():
    """"Water Calculator page
    using gender, weight, activity"""

    form = WaterCalculatorForm()

    if form.validate_on_submit():

        """Submit pressed"""
        weight = form.weight.data
        gender = form.gender.data
        activity = int(form.activity.data)

        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].weight = weight
            current_user.user_inputs[0].gender = gender
            current_user.user_inputs[0].activity = activity

            db_sess.merge(current_user)
            db_sess.commit()

        water_norm = calculate_water(weight, gender, activity)

        return render_template("water_calculator.html",
                               title='?????????????????????? ?????????????? ?????????? ????????', form=form,
                               water_norm=water_norm, active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from API and insert into form"""
        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()
        form.gender.data = inputs_json['user_inputs']['gender']
        form.weight.data = inputs_json['user_inputs']['weight']
        form.activity.data = str(inputs_json['user_inputs']['activity'])

    return render_template("water_calculator.html",
                           title='?????????????????????? ?????????????? ?????????? ????????', form=form,
                           active_calculator='active')


@app.route("/calculators/calories", methods=['GET', "POST"])
def calories_calculator_page():
    """"Calories Calculator page
    using gender, weight, height, age, activity"""

    form = CalorieCalculatorForm()

    if form.validate_on_submit():

        """Submit pressed"""
        weight = form.weight.data
        height = form.height.data
        age = form.age.data
        gender = form.gender.data
        activity = int(form.activity.data)

        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].weight = weight
            current_user.user_inputs[0].height = height
            current_user.user_inputs[0].age = age
            current_user.user_inputs[0].gender = gender
            current_user.user_inputs[0].activity = activity

            db_sess.merge(current_user)
            db_sess.commit()

        physical_activity_quotient = calculate_physical_activity_quotient(activity)
        calories_norm = calculate_calories(weight, height, age, gender, physical_activity_quotient)
        return render_template("calories_calculator.html",
                               title='?????????????????????? ?????????????? ?????????? ??????????????', form=form,
                               calories_norm=calories_norm, active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from API and insert into form"""
        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()
        form.gender.data = inputs_json['user_inputs']['gender']
        form.weight.data = inputs_json['user_inputs']['weight']
        form.height.data = inputs_json['user_inputs']['height']
        form.age.data = inputs_json['user_inputs']['age']
        form.activity.data = str(inputs_json['user_inputs']['activity'])

    return render_template("calories_calculator.html",
                           title='?????????????????????? ?????????????? ?????????? ??????????????', form=form,
                           active_calculator='active')


@app.route("/calculators/body_type", methods=['GET', "POST"])
def body_type_calculator_page():
    """"Body Type Calculator page
    using wrists"""

    form = BodyTypeCalculatorForm()

    if form.validate_on_submit():
        """Submit pressed"""
        wrists = form.wrists.data
        gender = form.gender.data
        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].wrists = wrists
            current_user.user_inputs[0].gender = gender
            db_sess.merge(current_user)
            db_sess.commit()
            """save results to the database"""
            current_user.user_results[0].body_type = calculate_body_type(wrists, gender)
            db_sess.merge(current_user)
            db_sess.commit()

        body_type = calculate_body_type(wrists, gender)

        return render_template("body_type_calculator.html",
                               title='?????????????????????? ???????? ????????????????????????', form=form,
                               body_type=body_type, active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from API and insert into form"""
        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()
        form.gender.data = inputs_json['user_inputs']['gender']
        form.wrists.data = inputs_json['user_inputs']['wrists']

    return render_template("body_type_calculator.html",
                           title='?????????????????????? ???????? ????????????????????????', form=form,
                           active_calculator='active')


@app.route("/calculators/body_fat", methods=['GET', "POST"])
def body_fat_calculator_page():
    """"Body Fat Calculator page
    using gender, waist, neck, hip"""
    form = BodyFatCalculatorForm()
    if form.validate_on_submit():

        """Submit pressed"""
        height = form.height.data
        waist = form.waist.data
        neck = form.neck.data
        hip = form.hip.data
        gender = form.gender.data

        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].height = height
            current_user.user_inputs[0].waist = waist
            current_user.user_inputs[0].neck = neck
            current_user.user_inputs[0].hip = hip
            current_user.user_inputs[0].gender = gender
            db_sess.merge(current_user)
            db_sess.commit()

        body_fat = calculate_body_fat_percent(height, waist, neck, hip, gender)

        return render_template("body_fat_calculator.html",
                               title='?????????????????????? ???????????????? ????????', form=form,
                               body_fat=body_fat, active_calculator='active')

    if current_user.is_authenticated:
        """Get user_inputs from API and insert into form"""
        inputs_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/inputs").json()
        form.gender.data = inputs_json['user_inputs']['gender']
        form.waist.data = inputs_json['user_inputs']['waist']
        form.height.data = inputs_json['user_inputs']['height']
        form.hip.data = inputs_json['user_inputs']['hip']
        form.neck.data = inputs_json['user_inputs']['neck']

    return render_template("body_fat_calculator.html",
                           title='?????????????????????? ???????????????? ????????', form=form, active_calculator='active')


@app.route('/recommendations', methods=['GET'])
def recommendations_page():
    """"recommendations page
    get query to API and return personal recommendations based on user data"""
    if current_user.is_authenticated:
        """User is authenticated 
        enable personal recommendations"""

        results_json = requests.get(f"{DOMAIN}/api/user/{current_user.id}/results").json()
        body_type = results_json['user_results']['body_type']
        return render_template('recommendations.html', title='??????????????????????', body_type=body_type,
                               active_recommendations='active')
    else:
        """User isn't authenticated 
        disable personal recommendations"""

        return render_template('recommendations.html',
                               title='??????????????????????', active_recommendations='active')


@app.route('/nutrition', methods=['GET', 'POST'])
def nutrition_page():
    """Nutrition page
    You can chose a product and check calories, proteins, fats, carbs in it"""

    global nutrition_dict
    form = NutritionSearchForm()

    if form.validate_on_submit():
        """Submit pressed
        show selected product data"""
        return render_template('nutrition.html', title='??????????????', nutrition_dict=nutrition_dict,
                               form=form, active_nutrition='active')
    """submit isn't pressed
     hide product data field"""
    return render_template('nutrition.html', title='??????????????', nutrition_dict=nutrition_dict,
                           form=form, active_nutrition='active')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """"Register user with Register Form
    Fields: name, email, about, password"""
    form = RegisterForm()
    # register button

    # random background image 1 of 5
    bg_index = randint(0, 4)

    if form.validate_on_submit():
        # check password match
        if form.password.data != form.password_again.data:
            # passwords isn't match
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="???????????? ???? ??????????????????",
                                   bg_index=bg_index)
        # new session
        db_sess = db_session.create_session()

        # check registered
        if db_sess.query(UserLogin).filter(UserLogin.email == form.email.data).first():
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="?????????? ???????????????????????? ?????? ????????",
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
            gender="??????????????",
            activity=2,
            wrists=18,
            waist=70,
            neck=40,
            hip=80
        )

        user_results = UserResults(
            BMI=22,
            body_type='????????????????'
        )

        user_login.user_inputs.append(user_inputs)
        db_sess.merge(user_login)
        db_sess.commit()

        user_login.user_results.append(user_results)
        db_sess.merge(user_login)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', title='??????????????????????', form=form, bg_index=bg_index)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """"Login using email and password
    Check correctness login and password
    After that, redirect to home(/) """
    # login form
    form = LoginForm()

    # random background image 1 of 5
    bg_index = randint(0, 4)

    # submit button
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # user search
        user = db_sess.query(UserLogin).filter(UserLogin.email == form.email.data).first()
        # check password
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # go home
            return redirect("/profile")

        # user error
        return render_template('login.html',
                               message="???????????????????????? ?????????? ?????? ????????????",
                               form=form,
                               bg_index=bg_index)

    # return template
    return render_template('login.html', title='??????????????????????', form=form, bg_index=bg_index)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    """"In this page user can edit all of him parameters"""

    form = ProfileForm()

    # submit button
    if form.validate_on_submit():
        """Submit pressed"""
        weight = form.weight.data
        height = form.height.data
        age = form.age.data
        gender = form.gender.data
        activity = int(form.activity.data)
        wrists = form.wrists.data
        waist = form.waist.data
        neck = form.neck.data
        hip = form.hip.data

        if current_user.is_authenticated:
            """user was authenticated
            save inputs to database"""
            db_sess = db_session.create_session()
            current_user.user_inputs[0].weight = weight
            current_user.user_inputs[0].height = height
            current_user.user_inputs[0].age = age
            current_user.user_inputs[0].gender = gender
            current_user.user_inputs[0].activity = activity
            current_user.user_inputs[0].wrists = wrists
            current_user.user_inputs[0].waist = waist
            current_user.user_inputs[0].neck = neck
            current_user.user_inputs[0].hip = hip

            db_sess.merge(current_user)
            db_sess.commit()

        return render_template("profile.html",
                               title='?????????????? ????????????????????????', form=form)

    if current_user.is_authenticated:
        """Get user_inputs from database and insert into form"""
        db_sess = db_session.create_session()
        current_user_inputs = db_sess.query(UserInputs).filter(
            UserInputs.user_id == current_user.id).first()

        form.weight.data = current_user_inputs.weight
        form.height.data = current_user_inputs.height
        form.age.data = current_user_inputs.age
        form.gender.data = current_user_inputs.gender
        form.activity.data = str(current_user_inputs.activity)
        form.wrists.data = current_user_inputs.wrists
        form.waist.data = current_user_inputs.waist
        form.neck.data = current_user_inputs.neck
        form.hip.data = current_user_inputs.hip

    return render_template("profile.html",
                           title='?????????????? ????????????????????????', form=form)


@app.route('/logout')
@login_required
def logout_page():
    """"Logout page
    kill current user session and redirect to home(/)"""
    logout_user()
    return redirect("/")


def create_nutrition_dict():
    """This function create list of tuples based on file pfcc.csv where saved data of products"""
    global nutrition_dict
    nutrition_dict = {}
    with open('static/csv/pfcc.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            if row:
                nutrition_dict[row[0]] = (row[1].replace(" ", ""), row[2].replace(
                    " ", ""), row[3].replace(" ", ""), row[4].replace(" ", ""))


if __name__ == '__main__':
    create_nutrition_dict()
    db_session.global_init("db/users.db")
    port = int(os.environ.get("PORT", 8080))
    # app.run(host='0.0.0.0', port=port)

    api.add_resource(restful_resources.InputsResource, '/api/user/<int:user_id>/inputs')
    api.add_resource(restful_resources.ResultsResource, '/api/user/<int:user_id>/results')

    # api.add_resource(restful_resources.UpdateUser, '/api/user')

    # api.add_resource(restful_resources.I, '/api/user_inputs/<int:user_id>')
    serve(app, host='0.0.0.0', port=port)
