from app import app
from db import db

#this file needs to be created because app.py will only work when __name__ __main__
#when we run from heroku without this .py, it will give us an error
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
