# Retrieve Flyby Observation and IDs based on Feature Name, Latitude/Longitude or Time

# Built in Python functions
from datetime import datetime, timedelta
import logging
import os

# External Python libraries (installed via pip install)
import pandas as pd
import numpy as np

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

### COLLECT FEATURE NAME INFORMATION FROM feature_name_details.csv #####
def latitudeLongitudeWithFeatureNameFromCSV():
	# Retrieve a list of Feature Names with a range of the associated latitude/longitude values
	#	Returns a Dictionary of Feature Name with feature details
	feature_name_dict = {}

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'feature_name_details.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)

	for index, row in flyby_dataframe.iterrows():
		if not pd.isnull(row).any(): # ignore rows where Latitude/Longitude are empty
			feature_name_dict[row["Feature Name"]] = {"Southmost Latitude": row["Southmost Latitude"],
													"Northmost Latitude": row["Northmost Latitude"], 
													"Eastmost Longitude": row["Eastmost Longitude"], 
													"Westmost Longitude": row["Westmost Longitude"],
													"Center Latitude": row["Center Latitude"],
													"Center Longitude": row["Center Longitude"]}

	return feature_name_dict

### RETURN FLYBY IDS FOR A GIVEN FEATURE NAME ##########################
def retrieveIDSByFeatureName(feature_name=None):
	# Retrieve a dictionary of flyby IDs and associated segment numbers
	#	Returns a Dictionary of Flyby IDs and a list of their segment numbers
	pydar.errorHandlingRetrieveIDSByFeature(feature_name=feature_name)

	feature_name_csv_dict = latitudeLongitudeWithFeatureNameFromCSV()
	feature_name = feature_name.title() # convert 'ligeria mare' to 'Ligeria Mare' to make input not sensitive to case

	if feature_name not in feature_name_csv_dict.keys():
		raise ValueError(f"Feature Name '{feature_name}' not in available in features list = {list(feature_name_csv_dict.keys())}")

	feature_dict = feature_name_csv_dict[feature_name]
	min_feature_latitude = min([feature_dict["Northmost Latitude"], feature_dict["Southmost Latitude"]])
	max_feature_latitude = max([feature_dict["Northmost Latitude"], feature_dict["Southmost Latitude"]])
	min_feature_longtidue = min([feature_dict["Eastmost Longitude"], feature_dict["Westmost Longitude"]])
	max_feature_longtidue = max([feature_dict["Eastmost Longitude"], feature_dict["Westmost Longitude"]])
	flyby_ids = retrieveIDSByLatitudeLongitudeRange(min_latitude=min_feature_latitude,
													max_latitude=max_feature_latitude,
													min_longitude=min_feature_longtidue,
													max_longitude=max_feature_longtidue)
	return flyby_ids

### RETURN FLYBY IDS FOR A SPECIFIC LATITUDE/LONGITUDE###################
def retrieveIDSByLatitudeLongitude(latitude=None, longitude=None):
	# Retrieve all FLyby Ids at a specific latitude/longitude
	#	Returns a Dictionary of Flyby IDs and a list of their segment numbers
	pydar.errorHandlingRetrieveIDSByLatitudeLongitude(latitude=latitude, longitude=longitude)

	# Runs range check, but the range is 0 for an exact spot
	flyby_ids = retrieveIDSByLatitudeLongitudeRange(min_latitude=latitude,
													max_latitude=latitude,
													min_longitude=longitude,
													max_longitude=longitude)
	return flyby_ids

### RETURN FLYBY IDS FOR A RANGE OF LATITUDE/LONGITUDES#################
def retrieveIDSByLatitudeLongitudeRange(min_latitude=None,
										max_latitude=None,
										min_longitude=None,
										max_longitude=None):
	# Retrieve all Flyby Ids that cover a specific latitude/longitude or within a range of latitude/longitudes
	#	Returns a Dictionary of Flyby IDs and a list of their segment numbers
	pydar.errorHandlingRetrieveIDSByLatitudeLongitudeRange(min_latitude=min_latitude,
														max_latitude=max_latitude,
														min_longitude=min_longitude,
														max_longitude=max_longitude)

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	flyby_ids = {} # {'flyby_id': ['S01', S03'] } 
	for index, row in swath_dataframe.iterrows():
		flyby = str(row['FLYBY ID'])
		# Check that given latitude/longitude range is within the flyby/segment's latitude/longitude
		if float(row["MINIMUM_LATITUDE (Degrees)"]) <= max_latitude and float(row["MAXIMUM_LATITUDE (Degrees)"]) >= min_latitude:
			min_id_longitude = min([float(row["EASTERNMOST_LONGITUDE (Degrees)"]), float(row["WESTERNMOST_LONGITUDE (Degrees)"])])
			max_id_longitude = max([float(row["EASTERNMOST_LONGITUDE (Degrees)"]), float(row["WESTERNMOST_LONGITUDE (Degrees)"])])
			if min_id_longitude <= min_longitude and max_id_longitude >= max_longitude:
				if flyby not in flyby_ids.keys():
					flyby_ids[flyby] = []
				segment_number = "S0" + str(row["SEGMENT NUMBER"])
				if segment_number not in flyby_ids[flyby]:
					flyby_ids[flyby].append(segment_number)

	if len(flyby_ids) == 0:
		logger.info(f"\n[WARNING]: No IDs found at latitude from {min_latitude} to {max_latitude} and longitude from {min_longitude} to {max_longitude}\n")

	return flyby_ids

### RETURN FLYBY IDS FOR A SPECIFIC TIME ###############################
def retrieveIDSByTime(year=None, doy=None, hour=None, minute=None, second=None, millisecond=None):
	# Retrieve Flyby IDs based on a single Timestamp of YYYY-DOYThh:mm:ss.sss
	#	Returns a Dictionary of Flyby IDs and a list of their segment numbers
	pydar.errorHandlingRetrieveIDSByTime(year=year, doy=doy, hour=hour, minute=minute, second=second, millisecond=millisecond)

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	# Retrieve using the time range function for the same time for start/end
	flyby_ids = retrieveIDSByTimeRange(start_year=year, 
										start_doy=doy,
										start_hour=hour, 
										start_minute=minute, 
										start_second=second, 
										start_millisecond=millisecond,
										end_year=year, 
										end_doy=doy,
										end_hour=hour, 
										end_minute=minute, 
										end_second=second, 
										end_millisecond=millisecond)

	return flyby_ids

### RETURN FLYBY IDS FOR A RANGE OF TIMES ###############################
def retrieveIDSByTimeRange(start_year=None, 
							start_doy=None,
							start_hour=None, 
							start_minute=None, 
							start_second=None, 
							start_millisecond=None,
							end_year=None, 
							end_doy=None,
							end_hour=None, 
							end_minute=None, 
							end_second=None, 
							end_millisecond=None):
	# Retrieve Flyby IDs based on a range of Timestamps YYYY-DOYThh:mm:ss.sss
	#	Returns a Dictionary of Flyby IDs and a list of their segment numbers

	pydar.errorHandlingRetrieveIDSByTimeRange(start_year=start_year, 
											start_doy=start_doy,
											start_hour=start_hour, 
											start_minute=start_minute, 
											start_second=start_second, 
											start_millisecond=start_millisecond,
											end_year=end_year, 
											end_doy=end_doy,
											end_hour=end_hour, 
											end_minute=end_minute, 
											end_second=end_second, 
											end_millisecond=end_millisecond)

	swath_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv')  # get file's directory, up one level, /data/*.csv
	swath_dataframe = pd.read_csv(swath_csv_file)

	# User Values: Set to a datetime object
	# Set default to 0 for all not defined values
	delta_hour = 0 if start_hour is None else start_hour
	delta_minute = 0 if start_minute is None else start_minute
	delta_second = 0 if start_second is None else start_second
	delta_millisecond = 0 if start_millisecond is None else start_millisecond

	start_of_year_start_datetime = datetime(year=start_year, month=1, day=1)
	start_datetime = start_of_year_start_datetime + timedelta(days=start_doy, hours=delta_hour, minutes=delta_minute, seconds=delta_second, milliseconds=delta_millisecond)

	delta_hour = 0 if end_hour is None else end_hour
	delta_minute = 0 if end_minute is None else end_minute
	delta_second = 0 if end_second is None else end_second
	delta_millisecond = 0 if end_millisecond is None else end_millisecond

	start_of_year_end_datetime = datetime(year=end_year, month=1, day=1)
	end_datetime = start_of_year_end_datetime + timedelta(days=end_doy, hours=delta_hour, minutes=delta_minute, seconds=delta_second, milliseconds=delta_millisecond)

	flyby_ids = {} # {'flyby_id': ['S01', S03']
	for index, row in swath_dataframe.iterrows():
		flyby = str(row['FLYBY ID'])

		start_time_year = int(row["START_TIME"][:4])
		start_time_doy = int(row["START_TIME"][5:8])
		start_time_hour = int(row["START_TIME"][9:11])
		start_time_minute = int(row["START_TIME"][12:14])
		start_time_second = int(row["START_TIME"][15:17])
		start_time_millisecond = int(row["START_TIME"][18:])

		stop_time_year = int(row["STOP_TIME"][:4])
		stop_time_doy = int(row["STOP_TIME"][5:8])
		stop_time_hour = int(row["STOP_TIME"][9:11])
		stop_time_minute = int(row["STOP_TIME"][12:14])
		stop_time_second = int(row["STOP_TIME"][15:17])
		stop_time_millisecond = int(row["STOP_TIME"][18:])
	
		# Row values: As datetime objects
		# Set default to 0 for all not defined values
		if start_hour is None: start_time_hour = 0
		if start_minute is None: start_time_minute = 0
		if start_second is None: start_time_second = 0
		if start_millisecond is None: start_time_millisecond = 0
	
		if end_hour is None: stop_time_hour = 0
		if end_minute is None: stop_time_minute = 0
		if end_second is None: stop_time_second = 0
		if end_millisecond is None: stop_time_millisecond = 0
	
		row_start_of_year_start_datetime = datetime(year=start_time_year, month=1, day=1)
		row_start_datetime = row_start_of_year_start_datetime + timedelta(days=start_time_doy, hours=start_time_hour, minutes=start_time_minute, seconds=start_time_second, milliseconds=start_time_millisecond)

		row_start_of_year_stop_datetime = datetime(year=stop_time_year, month=1, day=1)
		row_stop_datetime = row_start_of_year_stop_datetime + timedelta(days=stop_time_doy, hours=stop_time_hour, minutes=stop_time_minute, seconds=stop_time_second, milliseconds=stop_time_millisecond)

		if row_start_datetime <= end_datetime and row_stop_datetime >= start_datetime:
			# Add Flyby ID and Segment Number to returned dict
				if flyby not in flyby_ids.keys():
					flyby_ids[flyby] = []
				segment_number = "S0" + str(row["SEGMENT NUMBER"])
				if segment_number not in flyby_ids[flyby]:
					flyby_ids[flyby].append(segment_number)

	if len(flyby_ids) == 0:
		if start_datetime == end_datetime: # only display one datetime if both are the same
			logger.info(f"\n[WARNING]: No flyby IDs found at timestamp: {start_datetime}")
		else:
			logger.info(f"\n[WARNING]: No flyby IDs found at timestamp range: {start_datetime} to {end_datetime}")

	return flyby_ids

### RETURN FEATURE NAMES FOR A SPECIFIC LATITUDE/LONGTIUDE ##############
def retrieveFeaturesFromLatitudeLongitude(latitude=None, longitude=None):
	# Retrieve all Feature Names that at a specific latitude/longitude
	#	Returns a list of feature names
	pydar.errorHandlingRetrieveIDSByLatitudeLongitude(latitude=latitude, longitude=longitude)

	# Runs range check, but the range is 0 for an exact spot
	feature_names_list = retrieveFeaturesFromLatitudeLongitudeRange(min_latitude=latitude,
																	max_latitude=latitude,
																	min_longitude=longitude,
																	max_longitude=longitude)
	return feature_names_list

### RETURN FEATURE NAMES FOR A RANGE OF LATITUDE/LONGTIUDES #############
def retrieveFeaturesFromLatitudeLongitudeRange(min_latitude=None,
												max_latitude=None,
												min_longitude=None,
												max_longitude=None):
	# Retrieve all Feature Names that are within a range of latitude/longitude
	#	Returns a list of feature names
	pydar.errorHandlingRetrieveIDSByLatitudeLongitudeRange(min_latitude=min_latitude,
														max_latitude=max_latitude,
														min_longitude=min_longitude,
														max_longitude=max_longitude)

	feature_name_csv_dict = latitudeLongitudeWithFeatureNameFromCSV()
	feature_names_list = []

	def twoRangesIntersect(min_feature, max_feature, min_user, max_user):
		# Check if two ranges of latitude/longitudes overlap
		range1 = (min_feature <= max_user and min_feature >= min_user)
		range2 = (max_feature >= min_user and max_feature <= max_user)
		range3 = (min_feature <= min_user and max_feature >= max_user)
		intersectionFound = (range1 or range2 or range3)
		return intersectionFound

	for feature_name, position_dict in feature_name_csv_dict.items():
		min_feature_latitude = min([float(position_dict["Northmost Latitude"]), float(position_dict["Southmost Latitude"])])
		max_feature_latitude = max([float(position_dict["Northmost Latitude"]), float(position_dict["Southmost Latitude"])])
		if twoRangesIntersect(min_feature_latitude, max_feature_latitude, min_latitude, max_latitude):
			min_feature_longitude = min([float(position_dict["Westmost Longitude"]), float(position_dict["Eastmost Longitude"])])
			max_feature_longitude = max([float(position_dict["Westmost Longitude"]), float(position_dict["Eastmost Longitude"])])
			if twoRangesIntersect(min_feature_longitude, max_feature_longitude, min_longitude, max_longitude):
				feature_names_list.append(feature_name)

	if len(feature_names_list) == 0:
		logger.info(f"\n[WARNING]: No Features found at latitude from {min_latitude} to {max_latitude} and longitude from {min_longitude} to {max_longitude}\n")

	return feature_names_list
