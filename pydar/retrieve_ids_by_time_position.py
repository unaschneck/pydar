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
	swatch_flyby = []

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'sar_coverage_by_feature_name.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)

	for index, row in flyby_dataframe.iterrows():
		if str(row["Feature Name"]) != 'nan': # some feature names do not have associated names
			feature_name_list.append(row["Feature Name"])
		swatch_flyby.append(row["Swath Coverage"])

	return feature_name_list, swatch_flyby

def retrieveIDSByFeature(feature_name=None):
	pydar.errorHandlingRetrieveIDSByFeature(feature_name=feature_name)

	feature_name_list, swatch_flyby = sarCoverageFromCSV()
	feature_name = feature_name.title() # convert 'ligeria mare' to 'Ligeria Mare' to make input not sensitive to case

	if feature_name not in feature_name_list:
		logger.critical("Feature Name '{0}' not in available in features list = {1}".format(feature_name, feature_name_list))
		exit()

	index = feature_name_list.index(feature_name)
	flyby_ids = swatch_flyby[index].split(" ")

	return flyby_ids

def retrieveIDSByLatitudeLongitude(latitude=None, longitude=None, degrees_of_error=0):
	pydar.errorHandlingRetrieveIDSByLatitudeLongitude(latitude=latitude, longitude=longitude, degrees_of_error=degrees_of_error)

	logger.info("Latitude = {0}°, Longitude = {1}°, Degrees of Error = +/- {2}°".format(latitude, longitude, degrees_of_error))

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'sar_swath_details.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	flyby_ids = []

	if degrees_of_error != 0:
		latitude_range = [latitude - degrees_of_error, latitude, latitude + degrees_of_error]
		longitude_range = [longitude - degrees_of_error, longitude, longitude + degrees_of_error]
	else:
		latitude_range = [latitude]
		longitude_range = [longitude]

	for index, row in swath_dataframe.iterrows():
		for longitude in longitude_range:
			for latitude in latitude_range:
				if float(row['MIN – WEST LONGITUDE (DEG)']) <= longitude <= float(row['MAX – WEST LONGITUDE (DEG)']):
					if float(row['MIN – LATITUDE (DEG)']) <= latitude <= float(row['MAX – LATITUDE (DEG)']):
						flyby = 'T' + row["SWATH"] + "seg" + str(row["SEGMENT"])
						if flyby not in flyby_ids:
							flyby_ids.append(flyby)

	if len(flyby_ids) == 0:
		logger.info("\n[WARNING]: No flyby IDs found at latitude {0} and longitude {1}\n".format(latitude, longitude))

	return flyby_ids

def retrieveIDSByTime(timestamp=None):
	pydar.errorHandlingRetrieveIDSByTime(timestamp=timestamp)

	logger.info("TODO: Timestamp = {0}".format(timestamp))

	flyby_ids = []
	return flyby_ids
