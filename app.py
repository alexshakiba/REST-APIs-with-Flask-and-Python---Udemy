import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#change sqlite to whatever db you wnat
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') #first connects to Postgre, second is sqllite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off Flask-SQLALCH tracker, NOT the Alch tracker
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) #creates a new endoint /auth, when we call /auth, we send a
#username and passowrd, it calls the auth function and compare the password to what we recieved through the auth endpoint

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #name is same as above name
api.add_resource(ItemList, '/items') #name is same as above name
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register') #name is same as above name


if __name__ == '__main__':
    from db import db #importing down here because of "circular import"
    db.init_app(app)
    app.run(port=5000, debug=True)
