from netpix_app import create_app
from netpix_app.config import DevelopmentConfig
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from netpix_app import db, login_manager
from netpix_app.models import User, Account, Saved_Preferences
from netpix_app.auth.forms import SignupForm, LoginForm
from pathlib import Path
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta
import pandas as pd


app = create_app(DevelopmentConfig) #change config once developed (? - check submission advice from Week 6)
bp_main = Blueprint('main', __name__)
SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'saved_prefs.csv')
MY_SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'my_saved_prefs.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    title, dash_url = "Home", request.host_url + "/dashboard/"
    template_context = dict(title=title, dash_url=dash_url)
    users_saved = Saved_Preferences.query.filter_by(user_id=current_user.id).all()
    columns = ['tag','time-pref','genre-prefs','user-id']
    df = pd.DataFrame(columns=columns)
    df.to_csv(MY_SAVED_PREFS_FILEPATH)
    if not current_user.is_anonymous:
        username = current_user.username
        flash(f'Hi {username}. ')
    if users_saved != None:
        i = 0
        while i<len(users_saved):
            tag = users_saved[i].tag
            time_pref = users_saved[i].time_pref
            genre_prefs = users_saved[i].genre_prefs
            #genre_prefs = genre_prefs.split("+")
            user_id = users_saved[i].user_id
            saved_info = [tag, time_pref, genre_prefs, user_id]
            #saved_info = dict(tag=tag, time_pref=time_pref, genre_prefs=genre_prefs, user_id=user_id)
            #saved_prefs.append(saved_info)
            df = pd.DataFrame([saved_info])
            df.to_csv(MY_SAVED_PREFS_FILEPATH, mode='a', header=False)
            i = i+1

    if request.method == 'POST':
        df = pd.read_csv(SAVED_PREFS_FILEPATH)
        for index in df.index:
            username = df['username'][index]
            user = User.query.filter_by(username=username).first()
            if user != None:
                user_id = user.id
                tag = df['tag'][index]
                users_saved = Saved_Preferences.query.filter_by(user_id=user_id).all() 
                unique = True
                i = 0
                while i<len(users_saved):
                    if tag == users_saved[i].tag:
                        unique = False
                    i = i+1
                    pass
                if unique == True:
                    genre_prefs = df['genre-prefs'][index]
                    #genre_prefs = genre_prefs.split("+")
                    time_pref = int(df['time-pref'][index])
                    new_saved_pref = Saved_Preferences(tag=tag, time_pref=time_pref, genre_prefs=genre_prefs, user_id=user_id)
                    db.session.add(new_saved_pref)
                    db.session.commit()            
        return render_template('index.html', **template_context)
    return render_template('index.html', **template_context)

'''
@app.route('/', methods=['POST'])
def push_changes():
    flash('Page refreshed.')
    df = pd.read_csv(SAVED_PREFS_FILEPATH)
    for column in df[['tag']]:
        list_tags = df[column]
        list_time_prefs = df
        i = 0
        while i < len(list_tags):
            tag = list_tags[i]
            if Saved_Preferences.query.filter_by(tag=tag).first() == None: #if tag isn't in database ..yet
                tag = list_tags[i]
                pass
            i = i+1
        pass
    return render_template('index.html')
'''

if __name__ == '__main__':
    app.run(debug=True)