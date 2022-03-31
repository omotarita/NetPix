from flask import Flask, render_template
from netpix_app.auth import create_app
from netpix_app.config import DevelopmentConfig

app = create_app()

@app.route('/')
def hello_world():
    return render_template('index.html') #this should be the top half of the dashboard submitted for cw1

@app.route('/users/<username>')
def example11():
    return render_template('display_profile.html')

@app.route('/users/signup')
def example07():
    return render_template('create_account.html')

@app.route('/users/login')
def example08():
    return render_template('login.html')

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

if __name__ == '__main__':
    app.run(debug=True)