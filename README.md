# AI Weather Prediction Web App

This application collects weather data using an API, trains a machine learning model, and provides predictions through a REST API and a web interface built with Quasar.

---

## Environment Setup

### IMPORTANT
**Preparation:**
   - Delete any existing `.csv` files from the `WebScraper` or `TrainingModel/data` folders.
   - Delete any existing model files from the `TrainingModel/models` folder (if any).

1. Open a terminal in the TrainingModel directory and run:

   ```
   pip install -r requirements.txt
   ```

## Training The AI Model

To properly train the model, follow these steps:

1. **Scraping:**
   - From the `WebScraper` folder, run:

     ```
      openmeteo_scraper.py
     ```

2. **Move Data:**
   - Move the newly created `.csv` file to the `TrainingModel/data` folder.


3. **Train the Model:**
   - Run the training script:

     ```
      train_model.py
     ```

4. **Test the Model:**
   - After training, two model files will appear in `TrainingModel/models`.
   - Test the models by running:

     ```
      test/predict.py
     ```

---

## Running the Web Application (Quasar)

1. In the Quasar project terminal, run:

   ```
   npm init
   ```

   *(only if the project hasn't been initialized yet)*

2. Then start the REST-API:
    - Open new integrated terminal inside the REST-API Folder and run:
    ```
    .\app.py
    ```

3. Then start the development server:

   ```
   quasar dev
   ```

---

## Final Notes

The web application should now work correctly with the trained models and provide fairly accurate weather predictions.
