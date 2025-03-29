from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
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



if __name__ == '__main__':
    app.run(debug=True)