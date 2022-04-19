from netpix_app import create_app
from netpix_app.config import DevelopmentConfig
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy import insert, update, delete, or_
from sqlalchemy.exc import IntegrityError
from netpix_app import db, login_manager
from netpix_app.models import User, Account, Saved_Preferences, Blend
from netpix_app.auth.forms import SignupForm, LoginForm
from pathlib import Path
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta
import pandas as pd


app = create_app(DevelopmentConfig) #change config once developed (? - check submission advice from Week 6)
bp_main = Blueprint('main', __name__)
SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'saved_prefs.csv')
MY_SAVED_PREFS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'my_saved_prefs.csv')
MY_BLENDS_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'my_blends.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    title, dash_url = "Home", request.host_url + "/dashboard/"
    template_context = dict(title=title, dash_url=dash_url)
    columns = ['tag','time-pref','genre-prefs','user-id']
    df = pd.DataFrame(columns=columns)
    df.to_csv(MY_SAVED_PREFS_FILEPATH)
    blend_columns = ['tag','time-pref','genre-prefs','primary-user-id','secondary-user-id']
    df2 = pd.DataFrame(columns=blend_columns)
    df2.to_csv(MY_BLENDS_FILEPATH)
    if not current_user.is_anonymous:
        username = current_user.username
        flash(f'Hi {username}. ')
        users_saved = Saved_Preferences.query.filter_by(user_id=current_user.id).all()
        if users_saved != None:
            i = 0
            while i<len(users_saved):
                tag = users_saved[i].tag
                time_pref = users_saved[i].time_pref
                genre_prefs = users_saved[i].genre_prefs
                user_id = users_saved[i].user_id
                saved_info = [tag, time_pref, genre_prefs, user_id]
                df = pd.DataFrame([saved_info])
                df.to_csv(MY_SAVED_PREFS_FILEPATH, mode='a', header=False)
                i = i+1
        users_blends = Blend.query.filter(or_(Blend.primary_user_id==current_user.id, Blend.secondary_user_id==current_user.id)).all()
        if users_saved != None:
            i = 0
            while i<len(users_blends):
                tag = users_blends[i].tag
                time_pref = users_blends[i].time_pref
                genre_prefs = users_blends[i].genre_prefs
                primary_user_id = users_blends[i].primary_user_id
                secondary_user_id = users_blends[i].secondary_user_id
                blend_info = [tag, time_pref, genre_prefs, primary_user_id, secondary_user_id]
                df = pd.DataFrame([blend_info])
                df.to_csv(MY_BLENDS_FILEPATH, mode='a', header=False)
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


if __name__ == '__main__':
    app.run(debug=True)