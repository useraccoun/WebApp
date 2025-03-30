from flask import Flask, render_template, request
app = Flask(__name__) # Создание приложение. Так у нас flask знает где искать ресурсы(шаблоны и статические файлы)


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


@app.route('/register_handler', methods = ['POST'])
def reg_hand():
    username = request.form['username']
    password = request.form['password']
    check_password = request.form['check_password']
    print(username, password, check_password)


if __name__ == '__main__': # Делаем так, чтобы у нас всё автоматически подтягивалось при изменении чего либо
    app.run(debug=True)