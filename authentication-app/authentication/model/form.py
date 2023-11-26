from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    #username = StringField('Username')
    username = StringField(
        validators=[
            validators.InputRequired(),
            validators.Length(3, 20, message="Please provide a valid username"),
            validators.Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            )
        ]
    )
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    #username = StringField('Username')
    fullname = StringField('Fullname')
    username = StringField(
        validators=[
            validators.InputRequired(),
            validators.Length(3, 20, message="Please provide a valid username"),
            validators.Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            )
        ]
    )
    email = StringField(
        validators=[
            validators.InputRequired(), 
            validators.Email(), 
            validators.Length(1, 64)
        ]
    )
    #password = PasswordField('Password')
    password = PasswordField(validators=[validators.InputRequired(), validators.Length(8, 72)])
    confirm_password = PasswordField(
        validators=[
            validators.InputRequired(),
            validators.Length(8, 72),
            validators.EqualTo("password", message="Passwords must match !"),
        ]
    )
    submit = SubmitField('Submit')