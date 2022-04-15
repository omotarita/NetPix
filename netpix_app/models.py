from netpix_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    '''Class encapsulating all app users within the database'''
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    #first_name = db.Column(db.Text, nullable=False)
    #last_name = db.Column(db.Text, nullable=False)
    username = db. Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        #return f"{self.username} {self.email} {self.password}"
        return f"{self.id} {self.username} {self.email} {self.password}"
