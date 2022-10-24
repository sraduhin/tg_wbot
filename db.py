from datetime import datetime
from pymongo import MongoClient
import settings


client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id
        }
        db.users.insert_one(user)
    return user


def save_problem(db, user_id, problem_data):
    user = db.users.find_one({"user_id": user_id})
    problem_data['created'] = datetime.now()
    if 'problem' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'problem': [problem_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'problem': problem_data}}
        )
