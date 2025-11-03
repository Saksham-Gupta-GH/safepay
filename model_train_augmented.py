import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
import pickle
from datetime import datetime

print("Loading augmented dataset...")
df = pd.read_csv("transactions_augmented.csv")

print(f"Dataset shape: {df.shape}")
print(f"Fraud distribution: {df['Is_Fraud'].value_counts()}")

# Encode Card_Type
label_encoder_card = LabelEncoder()
df["Card_Type_Encoded"] = label_encoder_card.fit_transform(df["Card_Type"])

# Process Expiry_Date to extract features
def parse_expiry_date(expiry_str):
    """Parse MM/YY format and return months until expiry"""
    try:
        expiry_date = datetime.strptime(expiry_str, "%m/%y")
        current_date = datetime.now()
        months_diff = (expiry_date.year - current_date.year) * 12 + (expiry_date.month - current_date.month)
        return months_diff
    except:
        return 0

df["Months_Until_Expiry"] = df["Expiry_Date"].apply(parse_expiry_date)

# Create binary feature for expired cards
df["Is_Expired"] = (df["Months_Until_Expiry"] < 0).astype(int)

# Create binary feature for soon-to-expire cards (within 3 months)
df["Is_Soon_Expiry"] = ((df["Months_Until_Expiry"] >= 0) & (df["Months_Until_Expiry"] <= 3)).astype(int)

# Select features for the model
feature_columns = [
    "Age", 
    "Transaction_Amount", 
    "Account_Balance",
    "Card_Type_Encoded",
    "Months_Until_Expiry",
    "Is_Expired",
    "Is_Soon_Expiry"
]

X = df[feature_columns]
y = df["Is_Fraud"]

print(f"\nFeatures used: {feature_columns}")
print(f"Feature matrix shape: {X.shape}")

# Train-test split with 80/20 ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train the model
print("\nTraining Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=20, min_samples_split=10)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate evaluation metrics
print("\n" + "="*60)
print("MODEL EVALUATION METRICS")
print("="*60)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")

print("\n" + "-"*60)
print("CLASSIFICATION REPORT")
print("-"*60)
print(classification_report(y_test, y_pred, target_names=["Legit", "Fraudulent"]))

print("-"*60)
print("CONFUSION MATRIX")
print("-"*60)
cm = confusion_matrix(y_test, y_pred)
print(f"True Negatives:  {cm[0][0]}")
print(f"False Positives: {cm[0][1]}")
print(f"False Negatives: {cm[1][0]}")
print(f"True Positives:  {cm[1][1]}")
print()
print(cm)

# Feature importance
print("\n" + "-"*60)
print("FEATURE IMPORTANCE")
print("-"*60)
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance.to_string(index=False))

# Save the trained model and encoders
print("\n" + "="*60)
print("Saving model and encoders...")
with open("fraud_model_augmented.pkl", "wb") as f:
    pickle.dump(model, f)

with open("card_type_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder_card, f)

print("✓ Model saved as 'fraud_model_augmented.pkl'")
print("✓ Card type encoder saved as 'card_type_encoder.pkl'")
print("\nModel training completed successfully!")
print("="*60)
