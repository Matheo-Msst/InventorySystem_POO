from models.user_model import User

users_db = [
    User(1, "Alice", [
        ["", "", "","", "", "","", "", ""]
    ]),
    User(2, "Bob", [
        ["", "", "","", "", "","", "", ""]
    ]),
    User(3, "Charlie", [
        ["", "", "","", "", "","", "", ""]
    ]),
]

def get_all_users():
    return users_db

def get_user_by_id(user_id):
    for u in users_db:
        if u.id == user_id:
            return u
    return None
