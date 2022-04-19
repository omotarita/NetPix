from netpix_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    '''Class encapsulating all app users within the database'''
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    #first_name = db.Column(db.Text, nullable=False)
    #last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    account = db.relationship("Account", uselist=False, back_populates="user")
    saved_preferences = db.relationship("Saved_Preferences", uselist=False, back_populates="user")
    blend = db.relationship("Blend", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        #return f"{self.username} {self.email} {self.password}"
        return f"{self.id} {self.username} {self.email} {self.password}"

class Account(db.Model):
    '''Class representing users' public accounts within the database'''
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text, unique=True, nullable=True)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="account")
    friendship = db.relationship("Friendship", uselist=False, back_populates="account")
    #friends = #list of results from querying Friendship and reading users_friend for each result where user=username. Anytime a new friend is added, we db.commit a new Friendship and we insert friend's username into this list 
    #saved_preferences = db.relationship("Saved_Preferences", back_populates="account")
    #friends = db.relationship("Friends", back_populates="account")
    #blends = db.relationship("Blends", back_populates="account")
    #watched_movies = db.relationship("Watched_Movies", back_populates="account")

class Saved_Preferences(db.Model):
    '''Class representing users' saved preferences'''
    __tablename__ = "saved_preferences"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Text, nullable=False)
    time_pref = db.Column(db.Integer, nullable=False)
    genre_prefs = db.Column(db.Text, nullable=False) #we will convert from list to text to input into db then from text back to list to use
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="saved_preferences")

class Friendship(db.Model):
    '''Class representing users' friends'''
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text, nullable=False)
    users_friend = db.Column(db.Text, nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    account = db.relationship("Account", back_populates="friendship")

class Blend(db.Model): #two users can have the same blend
    '''Class representing all users' blends within the database''' #tbc
    __tablename__ = "blend_"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Text, nullable=False)
    time_pref = db.Column(db.Integer, nullable=False)
    genre_prefs = db.Column(db.Text, nullable=False)
    primary_user = db.Column(db.Text, nullable=False)
    secondary_user = db.Column(db.Text, nullable=False)
    primary_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    secondary_user_id = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="blend")

"""

class Watched_Movies(db.Model):
    '''Class representing users' watched movies'''
    __tablename__ = "watched_movies"
    id = db.Column(db.Integer, primary_key=True)
    account = db.relationship("Account", back_populates="saved_preferences")




"""