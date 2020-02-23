# Climate-APP

![surfs-up.png](Images/surfs-up.png)

So I decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, I need to do some climate analysis on the area. The following outlines what I need to do.

## Step 1 - Climate Analysis and Exploration

To begin,  I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database I found.

  * Chose a start date and end date for the trip. The vacation range is approximately 3-15 days total.

  * Used SQLAlchemy `create_engine` to connect to the sqlite database.

  * Used SQLAlchemy `automap_base()` to reflect the tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Designed a query to retrieve the last 12 months of precipitation data.

* Selected only the `date` and `prcp` values.

* Loaded the query results into a Pandas DataFrame and set the index to the date column.

* Sorted the DataFrame values by `date`.

* Plotted the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation.png)

* Used Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designed a query to calculate the total number of stations.

* Designed a query to find the most active stations.

* Designed a query to retrieve the last 12 months of temperature observation data (tobs).

    ![station-histogram](Images/station-histogram.png)

### Temperature Analysis

* Hawaii is reputed to enjoy mild weather all year. Was interested in knowing if there is a meaningful difference between the temperature in, for example, June and December?

* Identified the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Used t-test to determine whether the difference in the means, if any, is statistically significant.

- - -

## Step 2 - Climate App

After completing my initial analysis, I designed a Flask API based on the queries that I have just developed.

* Used FLASK to create my routes.

### Routes

* `/`

* `/api/v1.0/precipitation`

* `/api/v1.0/stations`

* `/api/v1.0/tobs`

* `/api/v1.0/<start>` 

* `/api/v1.0/<start>/<end>`

- - -
