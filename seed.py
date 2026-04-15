from app import app
from models import db, User, Note

with app.app_context():

   

    user1 = User.query.filter_by(username="john").first()
    if not user1:
        user1 = User(username="john")
        user1.set_password("1234")
        db.session.add(user1)

    user2 = User.query.filter_by(username="mary").first()
    if not user2:
        user2 = User(username="mary")
        user2.set_password("1234")
        db.session.add(user2)

    db.session.commit()

    print("Users ensured ✔")

    # Refresh users after commit (important for IDs)
    user1 = User.query.filter_by(username="john").first()
    user2 = User.query.filter_by(username="mary").first()

    

    if Note.query.count() == 0:

        note1 = Note(
            title="John Note 1",
            content="This is John's first note",
            user_id=user1.id
        )

        note2 = Note(
            title="John Note 2",
            content="Another note for John",
            user_id=user1.id
        )

        note3 = Note(
            title="Mary Note 1",
            content="Mary's personal note",
            user_id=user2.id
        )

        db.session.add_all([note1, note2, note3])
        db.session.commit()

        print("Notes created ✔")

    else:
        print("Notes already exist ✔")

    print("Seeding completed safely 🚀")