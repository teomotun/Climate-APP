import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start><br/>"
        f"/api/v1.0/startend/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculated the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Performed a query to retrieve the data and precipitation scores
    last_twelve = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in last_twelve:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get a list of stations
    results = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Get date one year from tobs
    max_tobs_last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    
    query_date = dt.date(2017, 8 ,18) - dt.timedelta(days=365)
    
    # Get tobs and date from a year ago
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)
    
    session.close()

     # Create a dictionary from the row data and append to a list of all_temp_normals
    t_normals = []
    for min_tobs, avg_tobs, max_tobs in results:
        temp_dict = {}
        temp_dict["Min TOBS"] = min_tobs
        temp_dict["AVG TOBS"] = avg_tobs
        temp_dict["MAX TOBS"] = max_tobs
        t_normals.append(temp_dict)
    
    return jsonify(t_normals)

@app.route("/api/v1.0/startend/<start>/<end>")
def startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_temp_normals
    t_normals = []
    for min_tobs, avg_tobs, max_tobs in results:
        temp_dict = {}
        temp_dict["Min TOBS"] = min_tobs
        temp_dict["AVG TOBS"] = avg_tobs
        temp_dict["MAX TOBS"] = max_tobs
        t_normals.append(temp_dict)
    
    return jsonify(t_normals)
if __name__ == '__main__':
    app.run(debug=True)
    
   
