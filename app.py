from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt



app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_Secret_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"


login_manager = LoginManager()

login_manager.login_view = 'login'

db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    

    if username and password:

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.enconde(user.password)):
            login_user(user)
            print(current_user.is_authenticated)

            return jsonify({"Message":"valid Credencials, Login you in"})

    return jsonify({"Message":"Invalid Credentials"}), 400

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"Message": "successfull Logout, bye bye"})


@app.post("/user")
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_pwd = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_pwd, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"Message": "User Created!!"})
    
    return jsonify({"Message": "Invalid input"}), 401

@app.get("/user/<int:id_user>")
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"Message":"User not found"}), 404


@app.put("/user/<int:id_user>")
@login_required
def update_user(id_user):
    user = User.query.get(id_user)
    data = request.json

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"Message":"Operation not allowed"}), 403

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()


        return jsonify({"Message": f"User {user.username} updated!"})

    return jsonify({"Message":"User not found"}), 404


@app.delete("/user/<int:id_user>")
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"Message":"Operation not allowed"}), 403
    
    if user and id_user != current_user.id:
        db.session.delete(user)
        db.commit()

        return {"Message": f"User {id_user} deleted"}
    
    return jsonify({"Message":"User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8080)