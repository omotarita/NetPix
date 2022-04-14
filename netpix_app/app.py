from flask import Flask, render_template, url_for, redirect, Blueprint
from netpix_app import create_app
from netpix_app.config import DevelopmentConfig
from netpix_app.auth.forms import SignupForm, LoginForm

app = create_app()
bp_main = Blueprint('main', __name__)


@app.route('/')
def index():
    return render_template('index.html', title="Home") #this should be the top half of the dashboard submitted for cw1

'''@app.route('/users/<username>')
def profile():
    return render_template('display_profile.html')'''
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.first_name.data
        return f"Thanks for registering. Welcome to Netpix"
    return render_template('signup.html', title='Create an Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    elif form.is_submitted and form.form_errors:
        return f"Failed!"
    return render_template('login.html', title='Sign In', form=form)

@app.route('/movie/choose/<sessionID>') #possibly remove... irrelevant ?
def example02():
    return render_template('login.html')  

@app.route('/movie/<movieID>')
def example04():
    return render_template('display_listing.html') #this should be the bottom half of the dashboard submitted for cw1

@app.route('/movie/results/<sessionID>')
def example03():
    return render_template('display_results.html') #this should be the top half of the dashboard submitted for cw1 (the bubble chart + a list)

@app.route('/users/blend/<blendID>')
def example05():
    return render_template('blend.html')

@app.route('/users/settings/<username>')
def example09():
    return render_template('display_settings.html')

@app.route('/users/saved/<username>')
def example10():
    return render_template('display_saved.html')

@app.route('/404')
def example12():
    return render_template('404.html')

@app.route('/505')
def example13():
    return render_template('505.html')
'''

if __name__ == '__main__':
    app.run(debug=True)