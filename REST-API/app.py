from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import pandas as pd

app = Flask(__name__)
CORS(app)  #Enables CORS for all routes

# Loads the model and the label encoder
model = load("../TrainingModel/models/weather_classifier_model.pkl")
label_encoder = load("../TrainingModel/models/weather_label_encoder.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Fetches JSON Data from the Request
        data = request.get_json()

        # Transform to DataFrame (must be in form dict -> list)
        df = pd.DataFrame([data])

        # Prediction
        prediction = model.predict(df)
        label = label_encoder.inverse_transform(prediction)

        return jsonify({"prediction": label[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)