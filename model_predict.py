import pickle
import numpy as np
from datetime import datetime

# Load augmented model and encoder
with open("fraud_model_augmented.pkl", "rb") as f:
    model_augmented = pickle.load(f)

with open("card_type_encoder.pkl", "rb") as f:
    card_type_encoder = pickle.load(f)

def predict_fraud(data):
    """Use augmented model for all predictions"""
    return predict_fraud_augmented(data)
    return "Fraudulent" if pred == 1 else "Legit"

def predict_fraud_augmented(data):
    """New prediction function using augmented model with expiry date and card type"""
    # Parse expiry date to get months until expiry
    def parse_expiry_date(expiry_str):
        try:
            expiry_date = datetime.strptime(expiry_str, "%m/%y")
            current_date = datetime.now()
            months_diff = (expiry_date.year - current_date.year) * 12 + (expiry_date.month - current_date.month)
            return months_diff
        except:
            return 0
    
    months_until_expiry = parse_expiry_date(data["Expiry_Date"])
    is_expired = 1 if months_until_expiry < 0 else 0
    is_soon_expiry = 1 if (months_until_expiry >= 0 and months_until_expiry <= 3) else 0
    
    # Encode card type
    card_type_encoded = card_type_encoder.transform([data["Card_Type"]])[0]
    
    # Create feature array
    features = np.array([[
        data["Age"],
        data["Transaction_Amount"],
        data["Account_Balance"],
        card_type_encoded,
        months_until_expiry,
        is_expired,
        is_soon_expiry
    ]])
    
    pred = model_augmented.predict(features)[0]
    return "Fraudulent" if pred == 1 else "Legit"
