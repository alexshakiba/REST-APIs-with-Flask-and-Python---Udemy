from werkzeug.security import safe_str_cmp
from models.user import UserModel

#used to authenticate a user
def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password): #same as below, but compares unicode, ASCII, etc differences
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
