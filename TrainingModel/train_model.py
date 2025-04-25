# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump

# Učitavanje podataka
df = pd.read_csv("data/rijeka_weather_openmeteo_5y_labeled.csv")

# 2. Inženjering značajki iz datuma
df["datetime"] = pd.to_datetime(df["datetime"])
df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month
df["day"] = df["datetime"].dt.day
df["weekday"] = df["datetime"].dt.weekday

# Uklanjanje nepotrebnih stupaca
X = df.drop(columns=["datetime", "weather_condition_label", "weather_code"])
y = df["weather_condition_label"]

# Label encoding ciljne varijable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Podjela na trening i test skup
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Treniranje modela
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluacija
predictions = model.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, predictions, target_names=label_encoder.classes_))
print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, predictions))

# Spremanje modela i label enkodera
dump(model, "models/weather_classifier_model.pkl")
dump(label_encoder, "models/weather_label_encoder.pkl")
print("\nModel i encoder su spremljeni u 'models/' direktorij.")
