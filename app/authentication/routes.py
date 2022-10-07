from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm

    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            print(name, email, password)

            user = User(name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {name}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            print(name, email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You logged in!', 'auth-success')
                return redirect(url_for('site.backlog'))
            else:
                flash("I'm sorry, Dave. I'm afraid I can't let you in.", 'auth-failed')
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))