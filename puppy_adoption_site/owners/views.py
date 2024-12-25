from flask import Blueprint, render_template, redirect, url_for
from puppy_adoption_site import db
from puppy_adoption_site.models import Owner
from puppy_adoption_site.owners.forms import AddOwnerForm

# Setting up the Blueprint

owners_blueprint = Blueprint('owners', __name__, template_folder='templates/owners')


# route the view using owners blueprint, here in route no need to say "/owners/add", it will be done in __init__.py file
@owners_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddOwnerForm()

    if form.validate_on_submit():
        name = form.name.data
        pup_id = form.pup_id.data

        new_owner = Owner(name, pup_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('puppies.list_of_puppies')) # it is set as "puppies.list" because when the blueprint is going to be registered, then it is registered on its name like in the above, name is set to "owners"
    return render_template('add_owners.html', form=form)
