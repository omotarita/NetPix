from flask import Blueprint, redirect, url_for, flash, request, render_template
from sqlalchemy.exc import IntegrityError
from netpix_app import db
from netpix_app.models import User
from netpix_app.auth.forms import SignupForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def index():
    return "This is the authentication section of the web app"#render_template('auth_index.html', title="Home") #this should be the top half of the dashboard submitted for cw1

'''@auth_bp.route('/users/<username>')
def profile():
    return render_template('display_profile.html')'''

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        print(user)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.username}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Create an Account', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    #elif form.is_submitted and form.form_errors:
    #    return f"Failed!"
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/movie/choose/<sessionID>') #possibly remove... irrelevant ?
def example02():
    return render_template('login.html')  

@auth_bp.route('/movie/<movieID>')
def example04():
    return render_template('display_listing.html') #this should be the bottom half of the dashboard submitted for cw1

@auth_bp.route('/movie/results/<sessionID>')
def example03():
    return render_template('display_results.html') #this should be the top half of the dashboard submitted for cw1 (the bubble chart + a list)

@auth_bp.route('/users/blend/<blendID>')
def example05():
    return render_template('blend.html')

@auth_bp.route('/users/settings/<username>')
def example09():
    return render_template('display_settings.html')

@auth_bp.route('/users/saved/<username>')
def example10():
    return render_template('display_saved.html')

@auth_bp.route('/404')
def example12():
    return render_template('404.html')

@auth_bp.route('/505')
def example13():
    return render_template('505.html')
