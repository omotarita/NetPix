from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from h11 import Data
from netpix_app import photos
from wtforms import StringField, PasswordField, EmailField, BooleanField, FormField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError
from netpix_app.models import User, Account
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
    username = StringField(label='Username', validators=[DataRequired()]) 
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)

    def validate_login(self, username, password):
        user = User.query.filter_by(username=username.data).first()
        password = generate_password_hash(password)
        if User.query.filter_by(username=username.data).first() is None:
            raise ValidationError('Incorrect password or username')
        elif User.check_password(user, password) == False:
            raise ValidationError('Incorrect password or username') ## this may not work...

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    #new_friend = ''

    '''
    def request_friend(self, username, new_friend):
        #if friend exists (their username is in database) and is not friends with self
        pass
    '''
