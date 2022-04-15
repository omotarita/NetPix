from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, FormField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError
from netpix_app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import random, string

class SignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=22)])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    accept_tos = BooleanField('I accept the terms and conditions', [validators.DataRequired()])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')
    
    def validate_details(self, username, email):
        alternative_user = username.data
        original_user = username.data
        users = User.query.filter_by(username=username.data).first()
        if users is not None:
            if User.query.filter_by(email=email.data).first() is None:
                while (User.query.filter_by(username=alternative_user).first()) is not None:
                    randomNumber = str(random.randint(0, 9))
                    randomLetter = random.choice(string.ascii_letters).lower()
                    alternative_user = original_user + randomNumber + randomLetter
                raise ValidationError(f'That username is already taken. Try {alternative_user} instead?')
            else:
                raise ValidationError('An account is already registered for that email address')

class LoginForm(FlaskForm):
    #email = EmailField(label='Email Login', validators=[DataRequired(), EqualTo('Email Address', message="There doesn't seem to be an account with this email address. Sign up instead?")])
    #email_or_username = StringField(label='Email or username', validators=[DataRequired()]) or EmailField(label='Email or username', validators=[DataRequired()])
    #email = EmailField(label='Email', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()]) 
    #password = PasswordField(label='Password Login', validators=[DataRequired(), EqualTo('Password', message="Forgotten your password?")])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)

    def validate_login(self, username, password):
        user = User.query.filter_by(username=username.data).first()
        password = generate_password_hash(password)
        if User.query.filter_by(username=username.data).first() is None:
            raise ValidationError('Incorrect password or username')
        elif User.check_password(user, password) == False:
            raise ValidationError('Incorrect password or username') ## this may not work...