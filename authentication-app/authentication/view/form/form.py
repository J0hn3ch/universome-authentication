from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname')
    role = StringField('Role')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')