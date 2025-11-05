from flask import Flask, render_template, request, redirect, url_for, session
import os
from pymongo import MongoClient, ReturnDocument
from encryption import encrypt_data, decrypt_data
from hashing import generate_hash, verify_password, hash_password
from digital_signature import sign_data, verify_signature
from model_predict import predict_fraud, predict_fraud_augmented
from homomorphic import get_paillier
from searchable_encryption import token_for
from datetime import datetime
import json

app = Flask(__name__)
# Read SECRET_KEY from environment for production safety. Do NOT commit secrets to git.
# Behavior:
# - If SECRET_KEY is set in the environment, use it.
# - If not set, generate a temporary key for local development (prints a warning).
import secrets
secret = os.environ.get("SECRET_KEY")
if not secret:
    # If running on Render or other production, raising is safer so you don't run with an ephemeral key.
    if os.environ.get("RENDER") or os.environ.get("HEROKU"):
        raise RuntimeError("SECRET_KEY environment variable not set. Set SECRET_KEY in Render environment settings.")
    # Development fallback (temporary key — not for production)
    print("WARNING: SECRET_KEY not set. Generating a temporary key for development.")
    secret = secrets.token_urlsafe(48)

app.secret_key = secret

# Paillier homomorphic instance (used for additive homomorphic operations)
paillier = get_paillier()

def get_db():
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/safepay")
    client = MongoClient(uri)
    db = client.get_default_database()
    if db is None:
        db = client["safepay"]

    return db

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        db = get_db()
        user = db.users.find_one({"username": username, "role": role})

        if user and verify_password(password, user.get("password", "")):
            session["user"] = username
            session["role"] = role
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials."
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    db = get_db()
    if session["role"] == "admin":
        users = list(db.users.find({}, {"_id": 0, "username": 1, "role": 1, "balance": 1}))
        txns = list(db.transactions.find({}, {"_id": 0}).sort("_id", -1))
        # Get transaction logs for admin
        logs = list(db.transaction_logs.find({}).sort("timestamp", -1).limit(100))
        return render_template("admin_dashboard.html", users=users, txns=txns, logs=logs)
    else:
        u = db.users.find_one({"username": session["user"]}, {"_id": 0, "balance": 1})
        balance = float(u.get("balance", 0.0)) if u else 0.0
        data = list(db.transactions.find({"customer_id": session["user"]}, {"_id": 0}).sort("_id", -1))
        # Get unread notifications for the user
        notifications = list(db.notifications.find({
            "user_id": session["user"],
            "read": False
        }).sort("timestamp", -1))
        return render_template("dashboard.html", data=data, balance=balance, notifications=notifications)

# ---------------- TRANSACTION ----------------
@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    if "user" not in session or session["role"] == "admin":
        return redirect("/")

    if request.method == "POST":
        base_data = {
            "Customer_ID": session["user"],
            "Receiver_ID": request.form["Receiver_ID"],
            "Customer_Name": request.form["Customer_Name"],
            "Gender": request.form["Gender"],
            "Age": int(request.form["Age"]),
            "State": request.form["State"],
            "City": request.form["City"],
            "Bank_Branch": request.form["Bank_Branch"],
            "Account_Type": request.form["Account_Type"],
            "Transaction_Amount": float(request.form["Transaction_Amount"]),
            "Transaction_Type": request.form["Transaction_Type"],
            "Merchant_Category": request.form["Merchant_Category"],
            "Expiry_Date": request.form["Expiry_Date"],
            "Card_Type": request.form["Card_Type"],
        }

        db = get_db()
        try:
            if base_data["Customer_ID"] == base_data["Receiver_ID"]:
                raise ValueError("Cannot transfer to self")

            sender = db.users.find_one({"username": base_data["Customer_ID"]})
            if not sender:
                raise ValueError("Sender not found")
            sender_balance = float(sender.get("balance", 0.0))
            amount = float(base_data["Transaction_Amount"])
            if amount <= 0 or sender_balance < amount:
                raise ValueError("Insufficient balance")

            receiver = db.users.find_one({"username": base_data["Receiver_ID"]})
            if not receiver:
                raise ValueError("Receiver not found")
            receiver_balance = float(receiver.get("balance", 0.0))

            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount

            updated_sender = db.users.find_one_and_update(
                {"username": base_data["Customer_ID"], "balance": sender_balance},
                {"$set": {"balance": new_sender_balance}},
                return_document=ReturnDocument.AFTER
            )
            if not updated_sender:
                raise ValueError("Concurrent update detected for sender; please retry")

            updated_receiver = db.users.find_one_and_update(
                {"username": base_data["Receiver_ID"], "balance": receiver_balance},
                {"$set": {"balance": new_receiver_balance}},
                return_document=ReturnDocument.AFTER
            )
            if not updated_receiver:
                db.users.update_one({"username": base_data["Customer_ID"]}, {"$set": {"balance": sender_balance}})
                raise ValueError("Concurrent update detected for receiver; please retry")

            data = dict(base_data)
            data["Account_Balance"] = sender_balance

            data_str = "|".join(str(v) for v in data.values())
            enc_data = encrypt_data(data_str)
            hash_value = generate_hash(data_str)
            signature = sign_data(hash_value)
            verified = verify_signature(hash_value, signature)

            # Use augmented model for fraud prediction
            fraud_status = predict_fraud_augmented(data)

            # Insert transaction
            # Store homomorphic encryption of amount (as integer cents) and searchable tokens
            try:
                amount_cents = int(round(amount * 100))
                amount_cipher = paillier.encrypt(amount_cents)
                amount_cipher_str = str(amount_cipher)
            except Exception:
                # Fallback: if homomorphic encryption fails, leave blank but do not interrupt transaction
                amount_cipher_str = ""

            try:
                customer_token = token_for(data["Customer_ID"])
                receiver_token = token_for(data["Receiver_ID"])
            except Exception:
                customer_token = ""
                receiver_token = ""

            txn_result = db.transactions.insert_one({
                "customer_id": data["Customer_ID"],
                "receiver_id": data["Receiver_ID"],
                "name": data["Customer_Name"],
                "gender": data["Gender"],
                "age": data["Age"],
                "state": data["State"],
                "city": data["City"],
                "branch": data["Bank_Branch"],
                "acc_type": data["Account_Type"],
                "amount": amount,
                "amount_enc": amount_cipher_str,
                "txntype": data["Transaction_Type"],
                "merchant": data["Merchant_Category"],
                "balance": new_sender_balance,
                "expiry_date": data["Expiry_Date"],
                "card_type": data["Card_Type"],
                "enc_data": enc_data,
                "hash": hash_value,
                "signature_hex": signature.hex() if hasattr(signature, "hex") else str(signature),
                "verified": bool(verified),
                "fraud_status": fraud_status,
                "customer_token": customer_token,
                "receiver_token": receiver_token
            })
            
            # Log transaction
            # Prepare payload for logging (kept plaintext for now, but also store encrypted/hash/signature for learning)
            log_payload = {
                "transaction_id": str(txn_result.inserted_id),
                "customer_id": data["Customer_ID"],
                "receiver_id": data["Receiver_ID"],
                "amount": amount,
                "sender_balance_before": sender_balance,
                "sender_balance_after": new_sender_balance,
                "receiver_balance_before": receiver_balance,
                "receiver_balance_after": new_receiver_balance,
                "expiry_date": data["Expiry_Date"],
                "card_type": data["Card_Type"],
                "fraud_flagged": fraud_status == "Fraudulent",
                "status": "completed",
                "can_undo": True,
                "timestamp": datetime.now().isoformat()
            }

            # Serialize payload deterministically for hashing/signing
            payload_str = json.dumps(log_payload, sort_keys=True, default=str)
            try:
                enc_payload = encrypt_data(payload_str)
            except Exception:
                enc_payload = ""

            try:
                hash_value = generate_hash(payload_str)
            except Exception:
                hash_value = ""

            try:
                signature = sign_data(hash_value)
                signature_hex = signature.hex() if hasattr(signature, "hex") else str(signature)
            except Exception:
                signature = b""
                signature_hex = ""

            try:
                verified = bool(verify_signature(hash_value, signature))
            except Exception:
                verified = False

            # Insert transaction log with additional metadata fields (non-destructive)
            db.transaction_logs.insert_one({
                "transaction_id": str(txn_result.inserted_id),
                "customer_id": data["Customer_ID"],
                "receiver_id": data["Receiver_ID"],
                "amount": amount,
                "timestamp": datetime.now(),
                "fraud_flagged": fraud_status == "Fraudulent",
                "status": "completed",
                "sender_balance_before": sender_balance,
                "sender_balance_after": new_sender_balance,
                "receiver_balance_before": receiver_balance,
                "receiver_balance_after": new_receiver_balance,
                "expiry_date": data["Expiry_Date"],
                "card_type": data["Card_Type"],
                "can_undo": True,
                # Learning/metadata fields
                "enc_data": enc_payload,
                "hash": hash_value,
                "signature_hex": signature_hex,
                "verified": verified
            })
        except Exception as e:
            return str(e)

        return render_template(
            "transaction_result.html",
            fraud_status=fraud_status,
            verified=verified,
            amount=amount,
            receiver=base_data["Receiver_ID"],
            new_balance=new_sender_balance
        )

    return render_template("transaction.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            initial_balance = float(request.form.get("balance", "50000"))
        except ValueError:
            initial_balance = 50000.0
        role = "user"

        db = get_db()
        exists = db.users.find_one({"username": username})
        if exists:
            return "Username already exists."

        db.users.insert_one({
            "username": username,
            "password": hash_password(password),
            "role": role,
            "balance": initial_balance
        })
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- UNDO TRANSACTION ----------------
@app.route("/undo_transaction/<log_id>", methods=["POST"])
def undo_transaction(log_id):
    if "user" not in session or session["role"] != "admin":
        return redirect("/")
    
    db = get_db()
    try:
        from bson.objectid import ObjectId
        
        # Get the transaction log
        log = db.transaction_logs.find_one({"_id": ObjectId(log_id)})
        if not log:
            return "Transaction log not found"
        
        if not log.get("can_undo", False):
            return "Transaction cannot be undone"
        
        if log.get("status") == "undone":
            return "Transaction already undone"
        
        # Reverse the transaction
        sender_id = log["customer_id"]
        receiver_id = log["receiver_id"]
        amount = log["amount"]
        
        # Get current balances
        sender = db.users.find_one({"username": sender_id})
        receiver = db.users.find_one({"username": receiver_id})
        
        if not sender or not receiver:
            return "User not found"
        
        sender_balance = float(sender.get("balance", 0.0))
        receiver_balance = float(receiver.get("balance", 0.0))
        
        # Reverse: add back to sender, deduct from receiver
        new_sender_balance = sender_balance + amount
        new_receiver_balance = receiver_balance - amount
        
        if new_receiver_balance < 0:
            return "Cannot undo: Receiver has insufficient balance"
        
        # Update balances
        db.users.update_one({"username": sender_id}, {"$set": {"balance": new_sender_balance}})
        db.users.update_one({"username": receiver_id}, {"$set": {"balance": new_receiver_balance}})
        
        # Create notifications for both sender and receiver
        timestamp = datetime.now()
        notification_message = f"Transaction of ₹{amount:.2f} has been reversed by admin. Your new balance is ₹{new_sender_balance:.2f}"
        receiver_notification = f"Transaction of ₹{amount:.2f} has been reversed by admin. Your new balance is ₹{new_receiver_balance:.2f}"

        # Prepare encrypted/hash/signature fields for notifications (for learning/demo only)
        try:
            notif_payload_1 = json.dumps({"user_id": sender_id, "message": notification_message, "timestamp": timestamp.isoformat(), "type": "transaction_reversal"}, sort_keys=True)
            notif_enc_1 = encrypt_data(notif_payload_1)
            notif_hash_1 = generate_hash(notif_payload_1)
            notif_sig_1 = sign_data(notif_hash_1)
            notif_sig_hex_1 = notif_sig_1.hex() if hasattr(notif_sig_1, "hex") else str(notif_sig_1)
            notif_verified_1 = bool(verify_signature(notif_hash_1, notif_sig_1))
        except Exception:
            notif_enc_1 = ""
            notif_hash_1 = ""
            notif_sig_hex_1 = ""
            notif_verified_1 = False

        try:
            notif_payload_2 = json.dumps({"user_id": receiver_id, "message": receiver_notification, "timestamp": timestamp.isoformat(), "type": "transaction_reversal"}, sort_keys=True)
            notif_enc_2 = encrypt_data(notif_payload_2)
            notif_hash_2 = generate_hash(notif_payload_2)
            notif_sig_2 = sign_data(notif_hash_2)
            notif_sig_hex_2 = notif_sig_2.hex() if hasattr(notif_sig_2, "hex") else str(notif_sig_2)
            notif_verified_2 = bool(verify_signature(notif_hash_2, notif_sig_2))
        except Exception:
            notif_enc_2 = ""
            notif_hash_2 = ""
            notif_sig_hex_2 = ""
            notif_verified_2 = False

        db.notifications.insert_many([
            {
                "user_id": sender_id,
                "message": notification_message,
                "timestamp": timestamp,
                "read": False,
                "type": "transaction_reversal",
                "enc_data": notif_enc_1,
                "hash": notif_hash_1,
                "signature_hex": notif_sig_hex_1,
                "verified": notif_verified_1
            },
            {
                "user_id": receiver_id,
                "message": receiver_notification,
                "timestamp": timestamp,
                "read": False,
                "type": "transaction_reversal",
                "enc_data": notif_enc_2,
                "hash": notif_hash_2,
                "signature_hex": notif_sig_hex_2,
                "verified": notif_verified_2
            }
        ])
        
        # Update log status
        db.transaction_logs.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": {
                "status": "undone",
                "can_undo": False,
                "undone_at": timestamp,
                "undone_by": session["user"]
            }}
        )
        
        return redirect(url_for("dashboard"))
    except Exception as e:
        return str(e)

# ---------------- MARK NOTIFICATION AS READ ----------------
@app.route("/mark_notification_read/<notification_id>", methods=["POST"])
def mark_notification_read(notification_id):
    if "user" not in session:
        return redirect("/")
        
    db = get_db()
    try:
        from bson.objectid import ObjectId
        db.notifications.update_one(
            {
                "_id": ObjectId(notification_id),
                "user_id": session["user"]
            },
            {"$set": {"read": True}}
        )
        return redirect(url_for("dashboard"))
    except Exception as e:
        return str(e)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
'''
start->admin->user->transaction->database
56, 85269.3
'''
