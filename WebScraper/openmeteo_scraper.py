import requests
import pandas as pd
from datetime import datetime, timedelta

# Parametri za Rijeku
latitude = 45.3271
longitude = 14.4422

# Datum: zadnjih 5 godina
end_date = datetime.today().date()
start_date = end_date - timedelta(days=10 * 365)

# Formatiraj datume za API
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# Open-Meteo API URL s weathercode
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_str}&end_date={end_str}"
    f"&hourly=temperature_2m,relative_humidity_2m,pressure_msl,"
    f"wind_speed_10m,wind_direction_10m,precipitation,weathercode"
    f"&timezone=Europe%2FBerlin"
)

# Dohvati podatke
response = requests.get(url)
data = response.json()

# Funkcija za pretvaranje weathercode u tekstualni label
def weathercode_to_label(code):
    mapping = {
        0: "Vedro",
        1: "Uglavnom vedro",
        2: "Djelomično oblačno",
        3: "Oblačno",
        45: "Magla",
        48: "Smrzavajuća magla",

        51: "Slaba rosulja",
        53: "Umjerena rosulja",
        55: "Jaka rosulja",

        56: "Slaba smrzavajuća rosulja",
        57: "Jaka smrzavajuća rosulja",

        61: "Slaba kiša",
        63: "Umjerena kiša",
        65: "Jaka kiša",

        66: "Slaba smrzavajuća kiša",
        67: "Jaka smrzavajuća kiša",

        71: "Slab snijeg",
        73: "Umjeren snijeg",
        75: "Jak snijeg",
        77: "Zrnca snijega",

        80: "Slabi pljuskovi",
        81: "Umjereni pljuskovi",
        82: "Jaki pljuskovi",

        85: "Slabi snježni pljuskovi",
        86: "Jaki snježni pljuskovi",

        95: "Grmljavina",
        96: "Grmljavina s malo tuče",
        99: "Grmljavina s jakom tučom"
    }
    return mapping.get(code, "Nepoznato")

# Kreiraj DataFrame
df = pd.DataFrame({
    "datetime": data["hourly"]["time"],
    "temperature_C": data["hourly"]["temperature_2m"],
    "humidity_percent": data["hourly"]["relative_humidity_2m"],
    "pressure_hPa": data["hourly"]["pressure_msl"],
    "wind_speed_kmh": data["hourly"]["wind_speed_10m"],
    "wind_direction_deg": data["hourly"]["wind_direction_10m"],
    "precipitation_mm": data["hourly"]["precipitation"],
    "weather_code": data["hourly"]["weathercode"]
})

# Dodaj tekstualnu oznaku vremena
df["weather_condition_label"] = df["weather_code"].apply(weathercode_to_label)

# Spremi CSV
df.to_csv("rijeka_weather_openmeteo_5y_labeled.csv", index=False)
print("✔️ CSV je uspješno spremljen s vremenskim uvjetima!")
