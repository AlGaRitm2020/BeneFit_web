from flask import Flask


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



main_app = MyApp(__name__, static_folder="./../static")
