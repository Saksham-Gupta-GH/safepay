import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Loading transactions.csv...")
df = pd.read_csv("transactions.csv")

print(f"Original dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Generate expiry dates
# 60% of fraudulent transactions have late expiry dates (past or near expiry)
# 40% of fraudulent transactions have normal expiry dates
# Non-fraudulent transactions mostly have normal expiry dates

np.random.seed(42)

def generate_expiry_date(is_fraud):
    """Generate credit card expiry date based on fraud status"""
    current_date = datetime.now()
    
    if is_fraud == 1:
        # 60% chance of late/expired card for fraud
        if np.random.random() < 0.6:
            # Generate expired or soon-to-expire date (within last 2 years or next 3 months)
            if np.random.random() < 0.5:
                # Expired card (past date)
                months_ago = np.random.randint(1, 24)
                expiry = current_date - timedelta(days=months_ago * 30)
            else:
                # Soon to expire (within 3 months)
                days_ahead = np.random.randint(1, 90)
                expiry = current_date + timedelta(days=days_ahead)
        else:
            # 40% normal expiry date
            months_ahead = np.random.randint(12, 60)
            expiry = current_date + timedelta(days=months_ahead * 30)
    else:
        # Non-fraud: mostly valid expiry dates (1-5 years ahead)
        months_ahead = np.random.randint(12, 60)
        expiry = current_date + timedelta(days=months_ahead * 30)
    
    # Format as MM/YY
    return expiry.strftime("%m/%y")

# Generate card types
# 5 unique values: Student, Merchant, Premium, Standard, Corporate
# 70% of frauds are done by Student or Merchant type

card_types = ["Student", "Merchant", "Premium", "Standard", "Corporate"]

def generate_card_type(is_fraud):
    """Generate card type based on fraud status"""
    if is_fraud == 1:
        # 70% chance of Student or Merchant for fraud
        if np.random.random() < 0.7:
            return np.random.choice(["Student", "Merchant"])
        else:
            return np.random.choice(["Premium", "Standard", "Corporate"])
    else:
        # Non-fraud: more evenly distributed
        weights = [0.15, 0.15, 0.25, 0.30, 0.15]  # Slightly favor Standard
        return np.random.choice(card_types, p=weights)

print("Generating expiry dates and card types...")
df["Expiry_Date"] = df["Is_Fraud"].apply(generate_expiry_date)
df["Card_Type"] = df["Is_Fraud"].apply(generate_card_type)

print(f"Augmented dataset shape: {df.shape}")
print("\nNew columns added:")
print(f"- Expiry_Date: {df['Expiry_Date'].nunique()} unique values")
print(f"- Card_Type: {df['Card_Type'].unique()}")

# Verify the distribution
fraud_data = df[df["Is_Fraud"] == 1]
non_fraud_data = df[df["Is_Fraud"] == 0]

print(f"\n--- Fraud Analysis ---")
print(f"Total fraudulent transactions: {len(fraud_data)}")
print(f"Card Type distribution in frauds:")
print(fraud_data["Card_Type"].value_counts())
fraud_student_merchant = fraud_data[fraud_data["Card_Type"].isin(["Student", "Merchant"])].shape[0]
print(f"Student/Merchant in frauds: {fraud_student_merchant} ({fraud_student_merchant/len(fraud_data)*100:.1f}%)")

print("\nSaving augmented dataset...")
df.to_csv("transactions_augmented.csv", index=False)
print("Augmented dataset saved as 'transactions_augmented.csv'")
