from flask import render_template, request, redirect, url_for, flash
from . import auth
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UpdateEmail, UpdatePassword, DeleteAccount, ResetPassword, ResetPasswordRequest
from ..models import User
from .. import db
from ..email import send_email
from ..flash_errors import flash_errors
import datetime

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data,
                    registration_date = datetime.datetime.now())
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

@auth.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    email_form = UpdateEmail()
    password_form = UpdatePassword()
    delete_form = DeleteAccount()
    user = User.query.get(current_user.id)
    if email_form.validate_on_submit():
        if user.verify_password(email_form.password.data):
            send_email(user.email, 'Updated email address',
                       'auth/email/address_change',
                       new_email = email_form.email.data)
            user.email = email_form.email.data
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm your account',
                       'auth/email/confirm', user = user, token = token)
            user.confirmed = False
            db.session.add(user)
            db.session.commit()
            flash('We\'ve sent you a confirmation email to your new address.')
            return redirect(url_for('main.root'))
        flash('Invalid password.')
    if password_form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user.verify_password(password_form.old_password.data):
            send_email(user.email, 'Updated password',
                       'auth/email/password_change', user = user)
            user.password = password_form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.root'))
        flash('Invalid password.')
    if delete_form.validate_on_submit():
        user = User.query.get(current_user.id)
        logout_user()
        db.session.delete(user)
        flash('Your account has been deleted.')
        return redirect(url_for('main.root'))

    return render_template('auth/settings.html',
                           email_form = email_form,
                           password_form = password_form,
                           delete_form = delete_form)

@auth.route('/reset', methods = ['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.root'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,
                       'Password reset request',
                       'auth/email/password_reset_request',
                       user = user,
                       token = token)
        flash('We\'ve sent you an email with instructions to reset your password.')
        return redirect(url_for('main.root'))
    return render_template('auth/reset_request.html', form = form)

@auth.route('/reset/<token>', methods = ['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.root'))
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.root'))
        if user.reset_password(token, form.password1.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.root'))
    return render_template('auth/reset_password.html', form=form, token=token)
