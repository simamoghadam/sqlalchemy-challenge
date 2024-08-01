# sqlalchemy-challenge
module_10_challenge

This challenge involves using a Python SQL toolkit and Object Relational Mapper (ORM) along with Flask to interact with and visualize data from the `hawaii.sqlite` database.

Files

climate_starter.ipynb: Interacts with the `hawaii.sqlite` database using SQLAlchemy and visualizes data with Pandas Plotting and Matplotlib. Includes querying the most active stations and listing them in descending order.

app.py: Sets up a Flask application to serve data from the `hawaii.sqlite` database. Includes a helper function for temperature range queries and ensures the session is closed after all routes are defined.

hawaii_measurements.csv: Raw Data
hawaii_stations.csv: Raw Data
hawaii.sqlite :sqlite database