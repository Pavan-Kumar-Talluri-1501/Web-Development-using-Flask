from flask import Blueprint, render_template,  redirect, url_for
from puppy_adoption_site import db
from puppy_adoption_site.models import Puppy
from puppy_adoption_site.puppies.forms import RegistrationForm, DeleteForm

puppies_blueprint = Blueprint("puppies", __name__, template_folder="templates/puppies")

@puppies_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup) # or you can write in multiple lines as name = form.name.data, new_pup = Puppy(name), db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('puppies.list_of_puppies'))
    return render_template('add.html', form=form)

@puppies_blueprint.route('/list')
def list_of_puppies():
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)

@puppies_blueprint.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        id = form.id.data
        pup = db.session.get(Puppy, id)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('puppies.list_of_puppies'))
    return render_template('delete.html', form=form)

# After adding the blueprints, register them in __init__.py file