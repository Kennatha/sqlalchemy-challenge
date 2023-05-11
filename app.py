# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #Query last 12 months of precipitaion data
    recent_prcp=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=dt.date(2016,8,23)).all()
    
    session.close()
    #add to dictionary
    prcp_list = []
    for date, prcp in recent_prcp:
       prcp_dict = {}
       prcp_dict["Date"] = date
       prcp_dict["Precipitation"] = prcp
       prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    #Query all station names
    all_stations=session.query(Station.station,Station.name).all()
    
    session.close()
    #add to dictionary
    station_list = []
    for station, name in all_stations:
        station_dict={}
        station_dict["Station"]=station
        station_dict["Name"]=name
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Query all station names
    greatest_tobs=session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00519281').\
    filter(Measurement.date>=dt.date(2016,8,23)).all()
    session.close()

    #add to dictionary
    tobs_list = []
    for date, tobs in greatest_tobs:
        tobs_dict={}
        tobs_dict["Date"]=date
        tobs_dict["Temperature"]=tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<int:start>")
def one_date(start):
    session = Session(engine)

    #Query all station names
    one_date=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=dt.date(start)).all()
    session.close()

    #add to dictionary
    one_date_list = []
    for minimum, maximum, avg in one_date:
        one_date_dict={}
        one_date_dict["Minimum Temperature"]=minimum
        one_date_dict["Maximum Temperature"]=maximum
        one_date_dict["Average Temperature"]=avg
        one_date_list.append(one_date_dict)

    return jsonify(one_date_list)

if __name__ == '__main__':
    app.run(debug=False)