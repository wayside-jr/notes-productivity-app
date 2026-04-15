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


if __name__ == "__main__":
    app.run(debug=True)