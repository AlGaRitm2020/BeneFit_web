"""NOT USED NOW"""

from flask import Flask


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
        self.domain = 'http://benefit2021.herokuapp.com'
        self.local_host = 'http://127.0.0.1:8080'
        self.domain = self.local_host


main_app = MyApp(__name__, static_folder="./../static")
