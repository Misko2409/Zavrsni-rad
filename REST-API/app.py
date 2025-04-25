from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)

# Učitaj model i label encoder
model = load("../TrainingModel/models/weather_classifier_model.pkl")
label_encoder = load("../TrainingModel/models/weather_label_encoder.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Dohvati JSON podatke iz zahtjeva
        data = request.get_json()

        # Pretvori u DataFrame (mora biti u obliku dict -> list)
        df = pd.DataFrame([data])

        # Predikcija
        prediction = model.predict(df)
        label = label_encoder.inverse_transform(prediction)

        return jsonify({"prediction": label[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)