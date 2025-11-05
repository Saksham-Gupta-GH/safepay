import os
from pymongo import MongoClient, ASCENDING
from hashing import hash_password

uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/safepay")
client = MongoClient(uri)
db = client.get_default_database()
if db is None:
    db = client["safepay"]


# Indexes
db.users.create_index([("username", ASCENDING)], unique=True)
db.transactions.create_index([("customer_id", ASCENDING)])
db.transactions.create_index([("receiver_id", ASCENDING)])
db.transactions.create_index([("fraud_status", ASCENDING)])
db.notifications.create_index([("user_id", ASCENDING)])
db.notifications.create_index([("read", ASCENDING)])

# Seed users if not present
seed_users = [
    {"username": "user1", "password": hash_password("1234"), "role": "user", "balance": 50000.0},
    {"username": "admin", "password": hash_password("admin"), "role": "admin", "balance": 50000.0},
    {"username": "saksham", "password": hash_password("hello123"), "role": "user", "balance": 50000.0},
]
for u in seed_users:
    if not db.users.find_one({"username": u["username"]}):
        db.users.insert_one(u)

print("MongoDB initialized and seeded!")

'''
python3 model_train_augmented.py
MONGODB_URI="<your-connection-string>" python3 db.py
MONGODB_URI="<your-connection-string>" python3 app.py
11/25, merchant
'''
