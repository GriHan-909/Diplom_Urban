from flask import Flask, render_template, request


app = Flask(__name__)
Users = {}
active_user = ''


@app.route('/', methods=['GET', 'POST'])
def home():
    global active_user
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
        Users[name] = {'age': int(age), 'height': int(
            height), 'weight': int(weight), 'gender': gender}
        active_user = name
    return render_template('base.html', name=name)


@app.route('/calculation/', methods=['GET', 'POST'])
def calc():
    value = 0
    if Users:
        user = Users[active_user]
        if request.method == 'GET':
            if user['gender'] == 'Мужской':
                value = 66.5 + (13.7 * user['weight']) + \
                    (5 * user['height']) - (6.8 * user['age'])
            elif user['gender'] == 'Женский':
                value = 655 + (9.6 * user['weight']) + \
                    (1.8 * user['height']) - (4.7 * user['age'])
        return render_template('calculation.html', value=round(value, 2))
    else:
        return render_template('calculation.html', value=round(value, 2))


if __name__ == '__main__':
    app.run(debug=True)
