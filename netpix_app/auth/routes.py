from queue import Empty
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, update, delete, or_
from netpix_app import db, login_manager, photos
from netpix_app.models import User, Account, Saved_Preferences, Friendship, Blend
from netpix_app.auth.forms import SignupForm, LoginForm, UpdateAccountForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path
import config
import os, random, string
import pandas as pd

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
posts = Blueprint('posts', __name__, template_folder='templates')
SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'saved_prefs.csv')


@auth_bp.route('/')
def index():
    return "This is the authentication section of the web app"

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
            login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
    elif form.is_submitted and form.form_errors:
        return flash("Failed!")
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
@login_required
def view_account(username=None):
    form = UpdateAccountForm()
    username = current_user.username
    account = Account.query.filter_by(username=username).first()
    email = account.email
    template_context = dict(username=username, email=email, first_name=None, last_name=None, photo_url=None, saved_prefs=None, friends=None, my_blends=None)
    if account.first_name != None:
        first_name = account.first_name
        template_context['first_name'] = first_name
    if account.last_name != None:
        last_name = account.last_name
        template_context['last_name'] = last_name
    if account.photo != None:
        photo_url = 'assets/images/' + account.photo
        template_context['photo_url'] = photo_url
    if request.method == 'POST' and form.validate_on_submit(): 
        if 'photo' in request.files:
            if request.files['photo'].filename != '':  
                filename = photos.save(request.files['photo'])
        if form.first_name.data != '':
            account.first_name = form.first_name.data
        if form.last_name.data != '':
            account.last_name = form.last_name.data
        if form.photo.data != None:
            account.photo = filename
        db.session.commit()
        return redirect(url_for('auth.view_account', form=form))
    users_saved = Saved_Preferences.query.filter_by(user_id=current_user.id).all()
    saved_prefs = []
    if users_saved != None:
        i = 0
        while i<len(users_saved):
            user_id = users_saved[i].user_id
            saved_info = dict(tag=gather_pref_info(users_saved, i)[0], time_pref=gather_pref_info(users_saved, i)[1], genre_prefs=gather_pref_info(users_saved, i)[2], user_id=user_id)
            saved_prefs.append(saved_info)
            i = i+1
    users_blends = Blend.query.filter_by(primary_user_id=current_user.id).all()
    my_blends = []
    if users_blends != None:
        i = 0
        while i<len(users_blends):
            blend_info = dict(tag=gather_pref_info(users_blends, i)[0], time_pref=gather_pref_info(users_blends, i)[1], genre_prefs=gather_pref_info(users_blends, i)[2])
            my_blends.append(blend_info)
            i = i+1
    template_context['my_blends'] = my_blends
    print("Template context blends")
    print(template_context['my_blends'])
    template_context['saved_prefs'] = saved_prefs
    template_context['friends'] = list_friends()
    print(template_context)
    return render_template('view_account.html', form=form, **template_context)

#here! 
@auth_bp.route('/users/find-friends', methods=['GET','POST'])
@login_required
def find_friends():
    template_context = dict(results=[], message="")
    all_friends = list_friends()
    if request.method == 'POST':
        if request.form["submit_button"] == 'Search':
            query = request.form.get("query")
            if (query == None) or (query == ""):
                results = []
                message = "Try searching a friend's username"
            else:
                matching_accounts = Account.query.filter(Account.username.contains(query))
                print("Here are the matching accounts")
                print(matching_accounts)
                results = []
                message = "No matching users :("
                if matching_accounts != []:
                    for account in matching_accounts:
                        if account.username != current_user.username:
                            username = account.username
                            email = account.email
                            account_info = dict(username=username, email=email, first_name=None, last_name=None, photo_url=None, not_friend=True)
                            if account.first_name != None:
                                first_name = account.first_name
                                account_info['first_name'] = first_name
                            if account.last_name != None:
                                last_name = account.last_name
                                account_info['last_name'] = last_name
                            if account.photo != None:
                                photo_url = 'assets/images/' + account.photo
                                account_info['photo_url'] = photo_url
                            i = 0
                            while i < len(all_friends):
                                this_friend = all_friends[i]
                                if (username == this_friend['friends_username']):
                                    account_info['not_friend'] = False
                                i = i+1
                            results.append(account_info)
                        else:
                            message = "It's just you!"  
            template_context['results'], template_context['message'] = results, message
        if request.form["submit_button"] == 'Add Friend':
            friends = False
            new_friend = request.form.get("new_friend")
            friend_user = User.query.filter_by(username=new_friend).first()
            if Friendship.query.filter_by(user=current_user.username, users_friend=new_friend).all() != []:
                friends = True
            if Friendship.query.filter_by(user=new_friend, users_friend=current_user.username).all() != []:
                friends = True
            if friends == False:
                friendship = Friendship(user=current_user.username, users_friend=new_friend, friend_id=friend_user.id, user_id=current_user.id)
                db.session.add(friendship)
                db.session.commit()
                flash("Added new friend!")
            else:
                flash("You're already friends!")
    return render_template('find_friends.html', **template_context)


@auth_bp.route('/users/blend', methods=['GET','POST'])
@login_required
def blend_friend():
    template_context = dict(friends=[], my_saved_prefs=[], friends_saved_prefs=[])
    template_context['friends'] = list_friends()
    if request.method == 'POST':
        if request.form["submit_button"] == 'Confirm':
            my_friend = request.form.get("my_friend")
            my_friend_user = User.query.filter_by(username=my_friend).first()
            template_context['my_saved_prefs'] = gather_saved(current_user)
            template_context['friends_saved_prefs'] = gather_saved(my_friend_user)            
        if request.form["submit_button"] == 'Blend':
            friend = Saved_Preferences.query.filter_by(tag=request.form.get("friends_pref")).first()
            friend_id = friend.user_id
            my_friend_user = User.query.filter_by(id=friend_id).first()
            if my_friend_user != None:
                my_friend = my_friend_user.username
                my_pref_tag = request.form.get("my_pref")
                friends_pref_tag = request.form.get("friends_pref")
                my_pref = Saved_Preferences.query.filter_by(tag=my_pref_tag).first()
                friends_pref = Saved_Preferences.query.filter_by(tag=friends_pref_tag).first()
                our_gen_prefs = my_pref.genre_prefs + friends_pref.genre_prefs
                our_time_pref = (my_pref.time_pref + friends_pref.time_pref)/2
                randomNumber = str(random.randint(0, 9))
                randomLetter = random.choice(string.ascii_letters).lower()
                tag = "Blend " + randomNumber + randomLetter + " (" + current_user.username + " + " + my_friend + ")"
                blend = Blend(tag=tag,time_pref=our_time_pref,genre_prefs=our_gen_prefs,primary_user=current_user.username,secondary_user=my_friend,primary_user_id=current_user.id, secondary_user_id=my_friend_user.id)
                db.session.add(blend)
                db.session.commit()
                flash("Blend complete!")
                flash("Click 'My Account' to see your blend, or click 'Home' to use it right away!")
                pass
            else:
                flash("Choose a friend first!")
    return render_template('blend.html', **template_context)

@auth_bp.route('/404')
def fn_404():
    return render_template('404.html')

@auth_bp.route('/505')
def fn_505():
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

def list_friends():
    friendships_list = Friendship.query.filter(or_(Friendship.user==current_user.username, Friendship.users_friend==current_user.username)).all()
    all_friends_info = []
    if friendships_list != None:
        i = 0
        while i<len(friendships_list):
            this_friend = friendships_list[i]
            if this_friend.user == current_user.username:
                friend_name = friendships_list[i].users_friend
            if this_friend.users_friend == current_user.username:
                friend_name = friendships_list[i].user
            friend_account = Account.query.filter_by(username=friend_name).first()
            if friend_account.photo != None:
               friend_photo_url = 'assets/images/' + friend_account.photo
            else:
               friend_photo_url = None
            friend_info = dict(friends_username=friend_name, friends_photo=friend_photo_url)
            all_friends_info.append(friend_info)
            i = i+1
    return all_friends_info

def gather_pref_info(users_blends, i):
    tag = users_blends[i].tag
    time_pref = users_blends[i].time_pref
    time = process_time(time_pref)
    genre_prefs = users_blends[i].genre_prefs
    genre_prefs = genre_prefs.split("+")
    return tag, time, genre_prefs

def process_time(time_pref):
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
    return time

def gather_saved(given_user):
    users_saved = Saved_Preferences.query.filter_by(user_id=given_user.id).all()
    users_preferences = []
    i = 0
    while i<len(users_saved):
        saved_pref = users_saved[i]
        tag = saved_pref.tag
        users_preferences.append(tag)
        i = i+1
    return users_preferences

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))