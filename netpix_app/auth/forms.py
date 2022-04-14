from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, FormField, validators
from wtforms.validators import DataRequired, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=22)])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    accept_tos = BooleanField('I accept the terms and conditions', [validators.DataRequired()])

class LoginForm(FlaskForm):
    #email = EmailField(label='Email Login', validators=[DataRequired(), EqualTo('Email Address', message="There doesn't seem to be an account with this email address. Sign up instead?")])
    #email_or_username = StringField(label='Email or username', validators=[DataRequired()]) or EmailField(label='Email or username', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[DataRequired()])
    #password = PasswordField(label='Password Login', validators=[DataRequired(), EqualTo('Password', message="Forgotten your password?")])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)