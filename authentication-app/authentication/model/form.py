from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators
from authentication.model.UserModel import User

class LoginForm(FlaskForm):
    #username = StringField('Username')
    #email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
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
    password = PasswordField(
        validators=[
            validators.InputRequired(), 
            validators.Length(min=8, max=72)
        ]
    )
    remember_me = BooleanField('Remember Me', default=False)
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

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
        
class RfidValidation(FlaskForm):
    uid = StringField(
        validators=[
            validators.InputRequired(),
            validators.Length(3, 20, message="Please provide a valid username"),
            validators.Regexp(
                "^[A-Za-z][A-Za-z0-9]*$",
                0,
                "Usernames must have only letters or " "numbers",
            )
        ]
    )

    submit = SubmitField('Check RFID')