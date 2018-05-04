import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'   #tell Alchemy the table name

    id = db.Column(db.Integer, primary_key=True) #there is a column called id with the column data
    username = db.Column(db.String(80)) #80 chars is limit of username
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #using this method we use cls instead of "User" - we don't need to hardcode the overlying class
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first() #can return the first because there is only one!

    @classmethod #using this method we use cls instead of "User" - we don't need to hardcode the overlying class
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
