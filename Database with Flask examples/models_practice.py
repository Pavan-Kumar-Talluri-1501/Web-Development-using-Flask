from models import app, db, Puppy, Toys, Owner

with app.app_context():
    db.create_all()

    # Creating puppies
    tommy = Puppy(name='Tommy')
    maxi = Puppy(name='Maxi')
    db.session.add_all([tommy, maxi])
    db.session.commit()

    # Creating owners
    john = Owner('John', maxi.id)
    db.session.add(john)
    db.session.commit()

    # Give toys to puppies
    toy1 = Toys('ball', maxi.id)
    toy2 = Toys('chew bone', tommy.id)
    db.session.add_all([toy1, toy2])
    db.session.commit()

    puppy_list = Puppy.query.all()
    tommy = Puppy.query.filter_by(name='Tommy').first()
    print(tommy)

    maxi.report_toys()