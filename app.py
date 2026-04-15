from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key" 

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "note productivity app"}

if __name__ == "__main__":
    app.run(debug=True)