from flask import Flask ,request , jsonify,session
from flask_migrate import Migrate
from models import db, bcrypt , User , Note

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key" 

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

@app.route("/")
def home():
    return {"message": "note productivity app"}


# sign up route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201

# login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        session["user_id"] = user.id
        return {"message": "Logged in successfully"}, 200

    return {"error": "Invalid username or password"}, 401


if __name__ == "__main__":
    app.run(debug=True)