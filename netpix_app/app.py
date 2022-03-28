from flask import Flask
from netpix_app.auth import create_app
from netpix_app.config import DevelopmentConfig

app = create_app()

@app.route('/')
def hello_world():
    return 'Netpix Homepage' #this should be the top half of the dashboard submitted for cw1

@app.route('/users/<username>')
def example11():
    pass

@app.route('/users/signup')
def example07():
    pass

@app.route('/users/login')
def example08():
    pass

@app.route('/movie/choose/<sessionID>') #possibly remove... irrelevant ?
def example02():
    pass  

@app.route('/movie/<movieID>')
def example04():
    pass #this should be the bottom half of the dashboard submitted for cw1

@app.route('/movie/results/<sessionID>')
def example03():
    pass #this should be the top half of the dashboard submitted for cw1 (the bubble chart + a list)


@app.route('/users/blend/<blendID>')
def example05():
    pass

@app.route('/users/settings/<username>')
def example09():
    pass

@app.route('/users/saved/<username>')
def example10():
    pass


if __name__ == '__main__':
    app.run(debug=True)