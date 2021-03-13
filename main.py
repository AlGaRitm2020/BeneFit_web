from flask import Flask, render_template

app = Flask(__name__)


# main
@app.route('/')
@app.route('/home/')
def main():
    astronauts = [
        'Ридли Скотт',
        'Энди Уир',
        'Марк Уотни',
        'Венката Капур',
        'Тедди Сандерс',
        'Шон Бин'
    ]

    return render_template('index.html', astronauts=astronauts)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
