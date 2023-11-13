from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from config import Config
from app.Controller.auth_forms import RegistrationForm
from app.Model.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.forms import LoginForm
from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Flash a success message and redirect to the index route
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('routes.index'))

    return render_template('register.html', form=form)


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.index'))

    return render_template('login.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
