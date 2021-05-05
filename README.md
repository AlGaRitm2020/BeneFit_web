![BeneFit](static/img/logo_original_cutted.png "BeneFit")
---------
Based on Flask<br>
Open [deployment](https://benefit2021.herokuapp.com) of this project (Heroku).


Introduction
------------
BeneFit is a website that helps you maintain a healthy lifestyle.<br>
There are sections
- calculators (BMI, heart rate, water norm, calories norm, body type, body fat)
- personal recommendations that dependence of user data
- nutrition page, where you can view proteins, fats, carbs and calories of any product

> Before getting personal recommendations you must be authorized

Frameworks and libraries
-----------
BeneFit using:
- Flask <https://flask.palletsprojects.com/en/1.1.x/>

- SQLAlchemy <http://www.sqlalchemy.org/>

- Heroku <https://heroku.com/>

- Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>

- Flask-login <https://flask-login.readthedocs.io/en/latest/>

- Flask-WTF <https://flask-wtf.readthedocs.io/en/stable/>

- WTForms <https://wtforms.readthedocs.io/en/2.3.x/>

- Bootstrap 5 <https://getbootstrap.com/>

- GIT <https://git-scm.com>

Installation
-----------
To run this project in your local environment


``` terminal
    1. Clone the repository:
    
      git clone https://github.com/AlGaRitm2020/BeneFit_web.git
      cd BeneFit_Web

    2. Create and activate a virtual environment:
    
          virtualenv env -p python3
          source env/bin/activate
    
    3. Install requirements:
    
          pip install -r requirements.txt
    
    4. Run the application:
    
          python application.py
    
    5. Go to http://127.0.0.1:8080
```

