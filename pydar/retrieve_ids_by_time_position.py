# Retrieve Flby Observation and IDs based on Latitude/Longitude or Time
import logging
import math
import os

import pandas as pd

import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def sarCoverageFromCSV():
	# Header: Feature Name, Center Latitude, Center Longitude, Feature Type, Feature Description, Swath Coverage
	feature_name_list = []
	latitude_list = []
	longitude_list = []

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'sar_coverage_by_feature_name.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)

	for index, row in flyby_dataframe.iterrows():
		if str(row["Feature Name"]) != 'nan': # some feature names do not have associated names
			feature_name_list.append(row["Feature Name"])
		latitude_list.append(row["Center Latitude"])
		longitude_list.append(row["Center Longitude"])

	return feature_name_list, latitude_list, longitude_list

def retrieveIDSByLatitudeLongitude(latitude=None, longitude=None, degrees_of_error=None):
	pydar.errorHandlingRetrieveIDSByLatitudeLongitude(latitude=latitude, longitude=longitude, degrees_of_error=degrees_of_error)

	feature_name_list, latitude_list, longitude_list = sarCoverageFromCSV()
	logger.info("Latitude = {0}, Longitude = {1}, Degrees of Error = {2}".format(latitude, longitude, degrees_of_error))

	flyby_ids = []
	return flyby_ids

def retrieveIDSByTime(timestamp=None):
	pydar.errorHandlingRetrieveIDSByTime(timestamp=timestamp)

	feature_name_list, latitude_list, longitude_list = sarCoverageFromCSV()
	logger.info("Timestamp = {0}".format(timestamp))

	flyby_ids = []
	return flyby_ids

def retrieveIDSByFeature(feature_name=None):
	pydar.errorHandlingRetrieveIDSByFeature(feature_name=feature_name)

	feature_name_list, latitude_list, longitude_list = sarCoverageFromCSV()
	logger.info("Feature Name = {0}".format(feature_name))

	if feature_name not in feature_name_list:
		logger.critical("Feature Name '{0}' not in available in features list = {1}".format(feature_name, feature_name_list))
		exit()

	flyby_ids = []
	return flyby_ids
