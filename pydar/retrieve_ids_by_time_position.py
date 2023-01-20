# Retrieve Flyby Observation and IDs based on Feature Name, Latitude/Longitude or Time
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
	pydar.errorHandlingRetrieveByLatitudeLongitude(latitude=latitude, longitude=longitude)

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
	pydar.errorHandlingRetrieveByLatitudeLongitudeRange(northernmost_latitude=northernmost_latitude,
														southernmost_latitude=southernmost_latitude,
														easternmost_longitude=easternmost_longitude,
														westernmost_longitude=westernmost_longitude)

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	flyby_ids = {} # {'flyby_id': ['seg1', seg4']
	for index, row in swath_dataframe.iterrows():
		flyby = str(row['FLYBY ID'])
		if float(row["MINIMUM_LATITUDE (Degrees)"]) <= southernmost_latitude and float(row["MAXIMUM_LATITUDE (Degrees)"]) >= northernmost_latitude:
			if float(row["EASTERNMOST_LONGITUDE (Degrees)"]) <= easternmost_longitude and float(row["WESTERNMOST_LONGITUDE (Degrees)"]) >= westernmost_longitude:
				if flyby not in flyby_ids.keys():
					flyby_ids[flyby] = []
				segment_number = "S0" + str(row["SEGMENT NUMBER"])
				if segment_number not in flyby_ids[flyby]:
					flyby_ids[flyby].append(segment_number)

	if len(flyby_ids) == 0:
		logger.info("\n[WARNING]: No flyby IDs found at latitude from {0} N to {1} S and longitude from {2} W to {3} E\n".format(northernmost_latitude,
																																southernmost_latitude,
																																westernmost_longitude,
																																easternmost_longitude))
		exit()

	return flyby_ids

def retrieveIDSByTime(year=None, month=None, day=None, hour=0, minute=0, second=0, millisecond=0):
	# TODO: Retrieve Flyby IDs based on a Timestamp
	pydar.errorHandlingRetrieveIDSByTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, millisecond=millisecond)

	logger.info("TODO: {0} year, {1} month, {2} day, {3} hour, {4} minute, {5} second, {6} millisecond".format(year,
																											month,
																											day,
																											hour,
																											minute,
																											second,
																											millisecond))

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	flyby_ids = {} # {'flyby_id': ['seg1', seg4']
	for index, row in swath_dataframe.iterrows():
		flyby = str(row['FLYBY ID'])
		'''
		if float(row["MINIMUM_LATITUDE (Degrees)"]) <= southernmost_latitude and float(row["MAXIMUM_LATITUDE (Degrees)"]) >= northernmost_latitude:
			if flyby not in flyby_ids.keys():
				flyby_ids[flyby] = []
			segment_number = "S0" + str(row["SEGMENT NUMBER"])
			if segment_number not in flyby_ids[flyby]:
				flyby_ids[flyby].append(segment_number)
		'''

	return flyby_ids

def retrieveFeaturesFromLatitudeLongitude(latitude=None, longitude=None):
	# Retrieve all Feature Names that at a specific latitude/longitude
	pydar.errorHandlingRetrieveByLatitudeLongitude(latitude=latitude, longitude=longitude)

	# Runs range check, but the range is 0 for an exact spot
	feature_names_list = retrieveFeaturesFromLatitudeLongitudeRange(northernmost_latitude=latitude,
																	southernmost_latitude=latitude,
																	easternmost_longitude=longitude,
																	westernmost_longitude=longitude)
	return feature_names_list


def retrieveFeaturesFromLatitudeLongitudeRange(northernmost_latitude=None,
												southernmost_latitude=None,
												easternmost_longitude=None,
												westernmost_longitude=None):
	# Retrieve all Feature Names that are within a range of latitude/longitude
	pydar.errorHandlingRetrieveByLatitudeLongitudeRange(northernmost_latitude=northernmost_latitude,
														southernmost_latitude=southernmost_latitude,
														easternmost_longitude=easternmost_longitude,
														westernmost_longitude=westernmost_longitude)

	feature_name_csv_dict = latitudeLongitudeWithFeatureNameFromCSV()
	feature_names_list = []

	for feature_name, position_dict in feature_name_csv_dict.items():
		if float(position_dict["Southernmost Latitude"]) >= southernmost_latitude and float(position_dict["Northernmost Latitude"]) <= northernmost_latitude:
			if float(position_dict["Easternmost Longitude"]) >= easternmost_longitude and float(position_dict["Westernmost Longitude"]) <= westernmost_longitude:
				feature_names_list.append(feature_name)

	if len(feature_names_list) == 0:
		logger.info("\n[WARNING]: No Features found at latitude from {0} N to {1} S and longitude from {2} W to {3} E\n".format(northernmost_latitude,
																																southernmost_latitude,
																																westernmost_longitude,
																																easternmost_longitude))
		exit()

	return feature_names_list
