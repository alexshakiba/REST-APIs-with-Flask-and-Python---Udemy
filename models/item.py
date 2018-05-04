import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'   #tell Alchemy the table name

    id = db.Column(db.Integer, primary_key=True) #there is a column called id with the column data
    name = db.Column(db.String(80)) #80 chars is limit of username
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #tablename.column_name
    store = db.relationship('StoreModel')

    def __init__(self,name,price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        #SELECT * FROM items WHERE name=name and returns the first row only
        #cls is ItemModel
        return cls.query.filter_by(name=name).first() #.query is defined from SQLAlch

    def save_to_db(self): #saving model to db/good for update & insert (upserting)
        db.session.add(self) #.session is a collection of objects we are writing to the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
