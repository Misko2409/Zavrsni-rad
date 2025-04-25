Firstly open the terminal and run "pip install -r requirements.txt" after that open up the WebScraper adjust the timespan of the 
dataset and then run it using the ".\openmeteo_scrapper.py". That will create a CSV File with the necessary data, after that we 
move the dataset to the "TrainingModel/data" File and run the .\train_model.py when the training completes we should have 2 new files in the
"TrainingModel/models". Those files will be used in our "REST-API/app.py"

We run the ".\app.py"

Afterwards inside the quasar-project terminal run "npm init" if needed and then "quasar dev"

The Web Application should work perfectly with the already trained program and should give us farely accurate results
