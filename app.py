from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_Secret_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


login_manager = LoginManager()

login_manager.login_view = 'login'

db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.post("/login")
def login():
    data = request.get_json()
    username = data.get["username"]
    password = data.get["password"]

    if username and password:

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)

            return jsonify({"Message":"valid Credencials, Login you in"})

    return jsonify({"Message":"Invalid Credentials"}), 400

@app.get("/hello-world")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, port=8080)