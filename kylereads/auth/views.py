from flask import render_template, request, redirect, url_for, flash
from . import auth
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import send_email

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash_errors(form)
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.root'))
        flash('Invalid username or password.')
    else:
        flash_errors(form)
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.root'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(error for error in flash_errors(form))
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your account',
                   'auth/email/confirm', user = user, token = token)
        flash('We\'ve sent you a confirmation email. You must confirm your address before proceeding.')
        return redirect(url_for('main.root'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('Your account has already been confirmed.')
        return redirect(url_for('main.root'))
    if current_user.confirm(token):
        flash('Your email address has been confirmed.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.root'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
       and not current_user.confirmed \
       and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.root'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    user = current_user
    token = current_user.generate_confirmation_token()
    send_email(user.email, 'Confirm your account',
               'auth/email/confirm', user = user, token = token)
    flash('We\'ve sent you a new confirmation email.')
    return redirect(url_for('main.root'))
