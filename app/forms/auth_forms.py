# Flask-WTF form module
from flask_wtf import FlaskForm
# Form fields
from wtforms import StringField, PasswordField, SubmitField
# Field validators
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Registration form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),               # Must not be empty
        Length(min=3, max=25)         # 3 to 25 characters
    ])
    email = StringField('Email', validators=[
        DataRequired(),               # Must not be empty
        Email()                       # Must be valid email
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),               # Must not be empty
        Length(min=6)                 # Minimum 6 characters
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),               # Must not be empty
        EqualTo('password')           # Must match password
    ])
    submit = SubmitField('Register')  # Submit button

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),               # Must not be empty
        Email()                       # Must be valid email
    ])
    password = PasswordField('Password', validators=[
        DataRequired()                # Must not be empty
    ])
    submit = SubmitField('Login')     # Submit button
