from flask import Blueprint
from flask import render_template
from netpix_app.auth.forms import SignupForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def index():
    return render_template('index.html', title="Home") #this should be the top half of the dashboard submitted for cw1

'''@auth_bp.route('/users/<username>')
def profile():
    return render_template('display_profile.html')'''

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.first_name.data
        return f"Welcome {name}!"
    return render_template('signup.html', title='Create an Account', form=form)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

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
