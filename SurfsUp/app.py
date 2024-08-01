from flask import Flask, jsonify
import numpy as np
import datetime as dt

# SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func, MetaData, Table

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///c:/Users/61433/Desktop/sqlalchemy-challenge/SurfsUp/hawaii.sqlite")

# Initialize the metadata
metadata = MetaData()

# Reflect the tables manually
measurement = Table('measurement', metadata, autoload_with=engine)
station = Table('station', metadata, autoload_with=engine)

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine, reflect=True)

# Print all table names in the database for verification
print(Base.classes.keys())

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a scoped session
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API! by Sima<br/>"
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        f"/&lt;start&gt;<br/>"
        f"/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/precipitation")
def precipitation():
    # Most recent date in dataset
    most_recent_date = "2017-08-23"
    recent_date_dt = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = recent_date_dt - dt.timedelta(days=365)

    # Query precipitation data
    precipitation_data = Session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    # Convert to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route("/stations")
def stations():
    # Query stations
    results = Session.query(Station.station).all()

    # Convert into a list of stations
    stations_list = [result[0] for result in results]

    return jsonify(stations_list)

@app.route("/tobs")
def tobs():
    # Most active station
    most_active_station = Session.query(
        Measurement.station,
        func.count(Measurement.station).label('count')
    ).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

    # Most recent date in dataset
    most_recent_date = "2017-08-23"
    recent_date_dt = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = recent_date_dt - dt.timedelta(days=365)

    # Query the last 12 months of temperature observation data for that station
    tobs_data = Session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == most_active_station).\
        order_by(Measurement.date).all()

    # Convert results to a list of dictionaries
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)

c
def calc_temps(start_date, end_date=None):
    if not end_date:
        results = Session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date).all()
    else:
        results = Session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return results[0]

@app.route("/<start>")
@app.route("/<start>/<end>")
def temperature_range(start, end=None):
    if end:
        temps = calc_temps(start, end)
    else:
        temps = calc_temps(start)

    temp_dict = {
        'TMIN': temps[0],
        'TAVG': temps[1],
        'TMAX': temps[2]
    }

    return jsonify(temp_dict)

# Close the session after all routes are defined
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    app.run(debug=True)