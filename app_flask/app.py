from db import init_db, add_user, get_user, del_user
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    name = None
    gender = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        gender = request.form.get('gender')

        if gender is None:
            return render_template('base.html', info='Не указан пол')

        add_user(name, int(age), int(height), int(weight), gender)

    return render_template('base.html', name=name)


@app.route('/calculation/', methods=['GET'])
def calc():
    value = 0
    active_user_name = request.args.get('name')
    user = get_user(active_user_name)
    if active_user_name:
        if user:
            gender = user['gender']
            if gender == 'Мужской':
                value = 66.5 + (13.7 * user['weight']) + \
                    (5 * user['height']) - (6.8 * user['age'])
            elif gender == 'Женский':
                value = 655 + (9.6 * user['weight']) + \
                    (1.8 * user['height']) - (4.7 * user['age'])
    del_user(active_user_name)
    return render_template('calculation.html', value=round(value, 2))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
