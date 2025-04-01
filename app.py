from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__) # Создание приложение. Так у нас flask знает где искать ресурсы(шаблоны и статические файлы)
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Оборачиваем наше приложение в класс SQLAlchemy


class User(db.Model): # Создание таблиц
    id = db.Column(db.Integer, primary_key=True) # Создание столбца id со значением integer. primary_key=True - означает, что столбцы будут идти по нумерации 1, 2, 3...
    login = db.Column(db.String(80), nullable=False) # Создание столбца login со значением String с ограничением 80 символов. nullable=False - означает, что если ничего не введется, то будет возвращать False
    password = db.Column(db.String(255), nullable=False) # Здесь ограничение 255, потому что у нас идёт шифрование пароля в бд.

with app.app_context(): # with - это по сути контекстное управление.  app.app_context() - создание контекста, без него нельзя взаимодействовать с базой данных
    db.create_all() # Создание таблиц, если их ещё нет. Эта штука взаимодействует с моделями, например сейчас с классом User

@app.route("/") # декоратор, чтобы сообщить Flask, какой URL должен вызывать нашу функцию.
def index():
    return render_template('index.html')


@app.route("/profile.html")
def profile():
    if "username" not in session: # Если наш аккаунт не сохранен в сессии(бд), то переходим на страницу login
        return redirect("/login.html")
    return render_template('profile.html')


@app.route("/main.html")
def main():
    return render_template('main.html')


@app.route("/login.html")
def login():
    return render_template('login.html')


@app.route("/register.html")
def register():
    return render_template('register.html')


@app.route('/register_handler', methods = ['POST', 'GET']) # Напрямую связываемся с front, '/register_handler' - это обработчик(action) в register.html. С methods идентичная ситуация
def reg_hand():
    if request.method == 'POST': # Получение данных формы, после сохраняем в бд
        username = request.form['username'] # Обращение к front, а именно к конкретному полю
        password = request.form['password']
        existing_user = User.query.filter_by(login=username).first() # Здесь мы делаем проверку, есть ли уже такой пользователь
        if existing_user:
            return "Ошибка: Такой пользователь уже есть!"

        hashed_password = generate_password_hash(password)
        new_user = User(login=username, password=hashed_password) # А тут создаём пользователя с передачей login и password. generate_password_hash(password) - это хэширование пароля
        db.session.add(new_user)
        db.session.commit() # Сохранение изменений в бд

        return redirect('/login.html')


@app.route('/login_handler', methods = ['POST'])
def login_hand():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(login=username).first()  # Находим запись в бд, по тому что ввели

    if user is None: # Если user равен None, значит, пользователя с таким логином нет в базе данных.
        return "Ошибка: Пользователь не найден!"

    if not check_password_hash(user.password, password):  # Проверка пароля на хэширование
        return "Ошибка: Неверный пароль!"

    session['username'] = user.login # Если логин и пароль верны, мы сохраняем в сессию, и пользователь остается авторизованным на сайте
    return redirect('/profile.html')





if __name__ == '__main__': # Делаем так, чтобы у нас всё автоматически подтягивалось при изменении чего либо
    app.run(debug=True)

