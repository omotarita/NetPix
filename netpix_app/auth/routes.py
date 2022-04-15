from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import IntegrityError
from netpix_app import db, login_manager
from netpix_app.models import User
from netpix_app.auth.forms import SignupForm, LoginForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

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
        #print(user)
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect password or username")
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=form.remember.data, duration=timedelta(minutes=1)) #check if it only works if remember me is selected...
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
    #elif form.is_submitted and form.form_errors:
    #    return f"Failed!"
    return render_template('login.html', title='Login', form=form)

@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#here! 
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
@login_required
def example05():
    return render_template('blend.html')

@auth_bp.route('/users/settings/<username>')
@login_required
def example09():
    return render_template('display_settings.html')

@auth_bp.route('/users/saved/<username>')
@login_required
def example10():
    return render_template('display_saved.html')

@auth_bp.route('/404')
def example12():
    return render_template('404.html')

@auth_bp.route('/505')
def example13():
    return render_template('505.html')

def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))