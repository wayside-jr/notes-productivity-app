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

# check profile with session
@app.route("/me", methods=["GET"])
def me():
    user = get_current_user()

    if not user:
        return {"error": "Not authenticated"}, 401

    return {
        "id": user.id,
        "username": user.username
    }, 200

# log out route
@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return {"message": "Logged out"}, 200

# get notes
@app.route("/notes", methods=["GET"])
def get_notes():
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    page = int(request.args.get("page", 1))
    per_page = 5

    notes = Note.query.filter_by(user_id=user.id).paginate(page=page, per_page=per_page)

    return {
        "notes": [
            {"id": n.id, "title": n.title, "content": n.content}
            for n in notes.items
        ],
        "total": notes.total,
        "pages": notes.pages
    }, 200

# create book
@app.route("/notes", methods=["POST"])
def create_note():
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    note = Note(
        title=data.get("title"),
        content=data.get("content"),
        user_id=user.id
    )

    db.session.add(note)
    db.session.commit()

    return {"message": "Note created"}, 201

# get a single note
@app.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get_or_404(id)

    if note.user_id != user.id:
        return {"error": "Forbidden"}, 403

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content
    }, 200

# update note
@app.route("/notes/<int:id>", methods=["PATCH"])
def update_note(id):
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get_or_404(id)

    if note.user_id != user.id:
        return {"error": "Forbidden"}, 403

    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)

    db.session.commit()

    return {"message": "Note updated"}, 200

# Delete route
@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get_or_404(id)

    if note.user_id != user.id:
        return {"error": "Forbidden"}, 403

    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)