import pandas as pd
from joblib import load
import datetime

# Učitavanje spremljenog modela i label encodera
model = load("models/weather_classifier_model.pkl")
label_encoder = load("models/weather_label_encoder.pkl")

# Ručni unos podataka
print("Unesi sljedeće podatke:")
temperature = float(input("Temperatura (C): "))
humidity = float(input("Vlaga (%): "))
pressure = float(input("Tlak (hPa): "))
wind_speed = float(input("Brzina vjetra (km/h): "))
wind_direction = float(input("Smjer vjetra (stupnjevi): "))
precipitation = float(input("Oborine (mm): "))
cloudcover = float(input("Oblačnost (%): "))
uv_index = float(input("UV indeks: "))
snowfall = float(input("Snježne oborine (mm): "))
is_day = int(input("Dan (1) ili noć (0): "))

# Datum i vrijeme (koristimo za izvlačenje hour, month, weekday)
datetime_str = input("Datum i vrijeme (YYYY-MM-DD HH:MM): ")
dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
hour = dt.hour
month = dt.month
day = dt.day
weekday = dt.weekday()

# Kreiranje DataFrame-a s jednim redom
X_new = pd.DataFrame([{
    "temperature_C": temperature,
    "humidity_percent": humidity,
    "pressure_hPa": pressure,
    "wind_speed_kmh": wind_speed,
    "wind_direction_deg": wind_direction,
    "precipitation_mm": precipitation,
    "cloudcover_percent": cloudcover,
    "uv_index": uv_index,
    "snowfall_mm": snowfall,
    "is_day": is_day,
    "hour": hour,
    "month": month,
    "day": day,
    "weekday": weekday
}])

# Predikcija
prediction_encoded = model.predict(X_new)
prediction_label = label_encoder.inverse_transform(prediction_encoded)

print(f"\n Predviđeno vremensko stanje: {prediction_label[0]}")
