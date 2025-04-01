from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__) # Создание приложение. Так у нас flask знает где искать ресурсы(шаблоны и статические файлы)
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
db = SQLAlchemy(app) # Оборачиваем наше приложение в класс SQLAlchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/") # декоратор, чтобы сообщить Flask, какой URL должен вызывать нашу функцию.
def index():
    return render_template('index.html')


@app.route("/profile.html")
def profile():
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(login=username).first()
        if existing_user:
            return "Ошибка: Такой пользователь уже есть!"


        new_user = User(login=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login.html')


@app.route('/login_handler', methods = ['POST', 'GET'])
def login_hand():
    if "username" in session:
        return redirect('/profile.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(login=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.id
            return redirect('/profile.html')

        return 'Ошибка: Неверный логин или пароль!'

    return render_template("login.html")



if __name__ == '__main__': # Делаем так, чтобы у нас всё автоматически подтягивалось при изменении чего либо
    app.run(debug=True)