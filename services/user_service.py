from models.user_model import User

users_db = [
    User(1, "Alice"),
    User(2, "Bob"),
    User(3, "yuno"),
    User(4, "Victor"),
    User(5, "Eve"),
    User(6, "Mallory")
]

def get_all_users():
    return users_db

def get_user_by_id(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return None
