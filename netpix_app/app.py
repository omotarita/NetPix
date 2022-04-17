from netpix_app import create_app
from netpix_app.config import DevelopmentConfig
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import IntegrityError
from netpix_app import db, login_manager
from netpix_app.models import User
from netpix_app.auth.forms import SignupForm, LoginForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import timedelta


app = create_app(DevelopmentConfig) #change config once developed (? - check submission advice from Week 6)
bp_main = Blueprint('main', __name__)


@app.route('/')
def index():
    title, dash_url = "Home", request.host_url + "/dashboard/"
    template_context = dict(title=title, dash_url=dash_url)
    if not current_user.is_anonymous:
        username = current_user.username
        flash(f'Hi {username}. ')
    return render_template('index.html', **template_context) #this should be the top half of the dashboard submitted for cw1


if __name__ == '__main__':
    app.run(debug=True)