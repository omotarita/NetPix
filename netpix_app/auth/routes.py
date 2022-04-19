from queue import Empty
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, update, delete
from netpix_app import db, login_manager, photos
from netpix_app.models import User, Account, Saved_Preferences, Friendship
from netpix_app.auth.forms import SignupForm, LoginForm, UpdateAccountForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path
import config
import os
import pandas as pd

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
posts = Blueprint('posts', __name__, template_folder='templates')
SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'saved_prefs.csv')


@auth_bp.route('/')
def index():
    return "This is the authentication section of the web app"#render_template('auth_index.html', title="Home") #this should be the top half of the dashboard submitted for cw1

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username=form.username.data).first()
            account = Account(username=form.username.data, email=form.email.data, user_id=user.id)
            db.session.add(account)
            db.session.commit()
            flash(f"Hello, {user.username}. You are signed up.")
            login_user(user)
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

@auth_bp.route('/users/account', methods=['GET', 'POST'])
@auth_bp.route('/users/account/<username>', methods=['GET', 'POST'])
@login_required #you have to be the user == <username> for this page to show 
def view_account(username=None): #provides functionality which shows account details and updates them if requested
    form = UpdateAccountForm()
    username = current_user.username
    account = Account.query.filter_by(username=username).first()
    email = account.email
    template_context = dict(username=username, email=email, first_name=None, last_name=None, photo_url=None, saved_prefs=None, friends=None)
    if account.first_name != None:
        first_name = account.first_name
        template_context['first_name'] = first_name
    if account.last_name != None:
        last_name = account.last_name
        template_context['last_name'] = last_name
    if account.photo != None:
        photo_url = 'assets/images/' + account.photo
        template_context['photo_url'] = photo_url
    #If updating account details..
    if request.method == 'POST' and form.validate_on_submit(): 
        if 'photo' in request.files:
            if request.files['photo'].filename != '':  
                filename = photos.save(request.files[
                                           'photo'])
        #account = Account.query.filter_by(username=username)
        if form.first_name.data != '': # If it isn't empty on submit, update
            account.first_name = form.first_name.data
        if form.last_name.data != '':
            account.last_name = form.last_name.data
        if form.photo.data != None:
            account.photo = filename
        db.session.commit() # Saves whatever changes have been made
        #filename = secure_filename(account.photo.filename)
        #account.photo.save(os.path.join(auth_bp.instance_path, 'photos', filename))
        return redirect(url_for('auth.view_account', form=form)) #should it return form results to be used in displaying user's profile?
    users_saved = Saved_Preferences.query.filter_by(user_id=current_user.id).all()
    saved_prefs = []
    if users_saved != None:
        i = 0
        while i<len(users_saved):
            tag = users_saved[i].tag
            time_pref = users_saved[i].time_pref
            hours = time_pref//60
            minutes= time_pref - (hours*60)
            if hours == 0:
                if minutes == 1:
                    time = f"Max: {minutes} minute"
                else:
                    time = f"Max: {minutes} minutes"
            elif hours == 1:
                if minutes ==1:
                    time = f"Max: {hours} hour and {minutes} minute"
                else:
                    time = f"Max: {hours} hour and {minutes} minutes"
            else:
                if minutes == 1:
                    time = f"Max: {hours} hours and {minutes} minute"
                else:
                    time = f"Max: {hours} hours and {minutes} minutes"
            genre_prefs = users_saved[i].genre_prefs
            genre_prefs = genre_prefs.split("+")
            user_id = users_saved[i].user_id
            saved_info = dict(tag=tag, time_pref=time, genre_prefs=genre_prefs, user_id=user_id)
            saved_prefs.append(saved_info)
            i = i+1
    friendships_list = Friendship.query.filter_by(user=current_user).all()
    friendships_list.append(Friendship.query.filter_by(users_friend=current_user).all())
    all_friends_info = []
    if friendships_list != None:
        i = 0
        while i<len(friendships_list):
            if friendships_list[i].user == current_user.username:
                friend_name = friendships_list[i].users_friend
            if friendships_list[i].users_friend == current_user.username:
                friend_name = friendships_list[i].user
            friend_account = Account.query.filter_by(username=friend_name).first()
            friend_photo_url = 'assets/images/' + friend_account.photo
            friend_info = dict(friends_username=friend_name, friends_photo=friend_photo_url)
            friend_info.append(all_friends_info)
            i = i+1
    template_context['saved_prefs'] = saved_prefs
    template_context['friends'] = all_friends_info
    return render_template('view_account.html', form=form, **template_context) #profile should include settings and saved, therefore subsequent two functions may be redundant

'''
@auth_bp.route('/users/account/<username>/settings')
@login_required #you have to be the user == <username> for this page to show 
def example09():
    return render_template('display_settings.html')

@auth_bp.route('/users/account/<username>/saved')
@login_required #you have to be the user == <username> for this page to show 
def example10():
    return render_template('display_saved.html')
'''
#here! 
#want to add functionality to search and add friends
@auth_bp.route('/users/find-friends', methods=['GET','POST'])
@login_required
def find_friends():
    #query = request.form['query']
    template_context = dict(results=[], message="")
    if request.method == 'POST':
        if request.form["submit_button"] == 'Search':
            query = request.form.get("query")
            if (query == None) or (query == ""):
                results = []
                message = "Try searching a friend's username"
                #matching_accounts = Account.query.filter(Account.username.contains(query)).all()
            else:
                matching_accounts = Account.query.filter(Account.username.contains(query))
                results = []
                if matching_accounts == []:
                    message = "No matching users :("
                else:
                    message = "No matching users :("
                    for account in matching_accounts:
                        if account.username != current_user.username:
                            username = account.username
                            email = account.email
                            account_info = dict(username=username, email=email, first_name=None, last_name=None, photo_url=None)
                            if account.first_name != None:
                                first_name = account.first_name
                                account_info['first_name'] = first_name
                            if account.last_name != None:
                                last_name = account.last_name
                                account_info['last_name'] = last_name
                            if account.photo != None:
                                photo_url = 'assets/images/' + account.photo
                                account_info['photo_url'] = photo_url
                            results.append(account_info)
                        else:
                            message = "It's just you!"
            template_context = dict(results=results, message=message)
        if request.form["submit_button"] == 'Add Friend':
            friends = False
            new_friend = request.form.get("new_friend")
            friend_user = User.query.filter_by(username=new_friend).first()
            if Friendship.query.filter_by(user=current_user, users_friend=friend_user).all() != None:
                friends = True
            if Friendship.query.filter_by(user=friend_user, users_friend=current_user).all() != None:
                friends = True
            if friends == False:
                friendship = Friendship(user=current_user.username, users_friend=new_friend, friend_id=friend_user.id, user_id=current_user.id)
                db.session.add(friendship)
                db.session.commit()
                flash("Added new friend!")
            else:
                flash("You're already friends!")
    return render_template('find_friends.html', **template_context)


@auth_bp.route('/users/blend')
@login_required
def blend_friend():
    pass
    return render_template('blend.html')

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