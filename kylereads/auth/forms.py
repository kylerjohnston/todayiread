from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo, DataRequired
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators = [InputRequired(), Length(1, 64),
                                               Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class RegistrationForm(Form):
    email = StringField('Email', validators = [InputRequired(),
                                              Length(1, 64),
                                              Email()])
    username = StringField('Username', validators=[
        InputRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators = [InputRequired(),
                                    EqualTo('password2',
                                    message = 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators = [InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already in use.')
    
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')

class UpdateEmail(Form):
    email = StringField('New email address', validators = [InputRequired(), Length(1, 64),
                                               Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already in use.')

class UpdatePassword(Form):
    old_password = PasswordField('Current password', validators = [InputRequired()])
    new_password = PasswordField('New password', validators = [InputRequired(),
                                    EqualTo('password2',
                                    message = 'Passwords must match.')])
    password2 = PasswordField('New password confirmation', validators = [InputRequired()])
    submit = SubmitField('Change password')

class DeleteAccount(Form):
    check1 = BooleanField('I am positive I want to delete my account.',
                          default = False, validators = [DataRequired()])
    check2 = BooleanField('I understand that all data associated with my account will be irrecoverably deleted.', default = False, validators = [DataRequired()])
    submit = SubmitField('Delete my account')

class ResetPasswordRequest(Form):
    email = StringField('Email address', validators = [InputRequired()])
    submit = SubmitField('Reset password')

class ResetPassword(Form):
    email = StringField('Email address', validators = [InputRequired()])
    password1 = PasswordField('New password',
                               validators = [
                                   InputRequired(),
                                   EqualTo('password2',
                                           message = 'Passwords must match.')])
    password2 = PasswordField('Confirm password',
                              validators = [InputRequired()])
    submit = SubmitField('Update password')
