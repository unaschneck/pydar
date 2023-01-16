# Retrieve Flby Observation and IDs based on Latitude/Longitude or Time
import logging
import math
import os

import pandas as pd
import numpy as np

import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def latitudeLongitudeWithFeatureNameFromCSV():
	# Retrieve a list of Feature Names with a range of the associated latitude/longitude values
	feature_name_dict = {}

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'feature_name_details.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)

	for index, row in flyby_dataframe.iterrows():
			feature_name_dict[row["Feature Name"]] = {"Southernmost Latitude": row["Southernmost Latitude"],
													"Northernmost Latitude": row["Northernmost Latitude"], 
													"Easternmost Longitude": row["Easternmost Longitude"], 
													"Westernmost Longitude": row["Westernmost Longitude"],
													"Center Latitude": row["Center Latitude"],
													"Center Longitude": row["Center Longitude"]}

	return feature_name_dict

def retrieveIDSByFeatureName(feature_name=None):
	pydar.errorHandlingRetrieveIDSByFeature(feature_name=feature_name)

	feature_name_csv_dict = latitudeLongitudeWithFeatureNameFromCSV()
	feature_name = feature_name.title() # convert 'ligeria mare' to 'Ligeria Mare' to make input not sensitive to case

	if feature_name not in feature_name_csv_dict.keys():
		logger.critical("Feature Name '{0}' not in available in features list = {1}".format(feature_name, list(feature_name_csv_dict.keys())))
		exit()

	feature_dict = feature_name_csv_dict[feature_name]
	flyby_ids = retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=feature_dict["Northernmost Latitude"],
													southernmost_latitude=feature_dict["Southernmost Latitude"],
													easternmost_longitude=feature_dict["Easternmost Longitude"],
													westernmost_longitude=feature_dict["Westernmost Longitude"])
	return flyby_ids

def retrieveIDSByLatitudeLongitude(latitude=None, longitude=None):
	# Retrieve all FLyby Ids at a specific latitude/longitude
	pydar.errorHandlingRetrieveIDSByLatitudeLongitude(latitude=latitude, longitude=longitude)

	# Runs range check, but the range is 0 for an exact spot
	flyby_ids = retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=latitude,
													southernmost_latitude=latitude,
													easternmost_longitude=longitude,
													westernmost_longitude=longitude)
	return flyby_ids

def retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=None,
										southernmost_latitude=None,
										easternmost_longitude=None,
										westernmost_longitude=None):
	# Retrieve all Flyby Ids that cover a specific latitude/longitude or within a range of latitude/longitudes
	pydar.errorHandlingRetrieveIDSByLatitudeLongitudeRange(northernmost_latitude=northernmost_latitude,
														southernmost_latitude=southernmost_latitude,
														easternmost_longitude=easternmost_longitude,
														westernmost_longitude=westernmost_longitude)

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	flyby_ids = []
	for index, row in swath_dataframe.iterrows():
		flyby = str(row['FLYBY ID']) + "seg" + str(row["SEGMENT NUMBER"])
		if flyby not in flyby_ids:
			if float(row["MINIMUM_LATITUDE (Degrees)"]) <= southernmost_latitude and float(row["MAXIMUM_LATITUDE (Degrees)"]) >= northernmost_latitude:
				if float(row["EASTERNMOST_LONGITUDE (Degrees)"]) <= easternmost_longitude and float(row["WESTERNMOST_LONGITUDE (Degrees)"]) >= westernmost_longitude:
					flyby_ids.append(flyby)

	if len(flyby_ids) == 0:
		logger.info("\n[WARNING]: No flyby IDs found at latitude {0} and longitude {1}\n".format(latitude, longitude))

	return flyby_ids

def retrieveIDSByTime(timestamp=None):
	pydar.errorHandlingRetrieveIDSByTime(timestamp=timestamp)

	logger.info("TODO: Timestamp = {0}".format(timestamp))

	flyby_ids = []
	return flyby_ids
