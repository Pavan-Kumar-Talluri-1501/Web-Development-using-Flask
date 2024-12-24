# Performing crud operations

from setupdb import app, db, Puppy

with app.app_context():

    # Create a puppy entry

    my_puppy = Puppy('tommy', 5)
    db.session.add(my_puppy)
    db.session.commit()

    # READ the tables and get the info

    all_puppies = Puppy.query.all()
    print(all_puppies)

    # Selecting by id
    first_puppy = db.session.get(Puppy, 1)
    print(first_puppy.name)

    # Filters, filtering puppies with their attributes like name and age
    pup_sam = Puppy.query.filter_by(name='Sammy')
    print(pup_sam.all())

    # UPDATE the existing entry
    second_pup = db.session.get(Puppy, 2)
    second_pup.age = 7
    db.session.add(second_pup)
    db.session.commit()

    # DELETE an entry
    third_pup = db.session.get(Puppy, 3)
    db.session.delete(third_pup)
    db.session.commit()

    all_puppies = Puppy.query.all()
    print(all_puppies)