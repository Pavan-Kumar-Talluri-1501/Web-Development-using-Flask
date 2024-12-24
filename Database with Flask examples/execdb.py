from setupdb import app, db, Puppy

with app.app_context():
    db.create_all()

    sam = Puppy('sammy', 3)
    maxi = Puppy('maxi', 4)

    print(sam.id)
    print(maxi.id)

    db.session.add_all([sam, maxi])
    db.session.commit()

    print(sam.id)
    print(maxi.id)