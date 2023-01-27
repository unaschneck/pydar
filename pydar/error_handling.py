########################################################################
# ERROR CATCHES AND LOGGING
########################################################################
import logging
import os
import csv

import pandas as pd

import pydar

## Logging set up for .CRITICAL
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def errorHandlingExtractFlybyDataImages(flyby_observation_num=None,
										flyby_id=None,
										segment_num=None,
										additional_data_types_to_download=[],
										resolution=None,
										top_x_resolutions=None):
	# Error Handling for extract_flyby_parameters variables
	avaliable_flyby_id, avaliable_observation_numbers = pydar.getFlybyData()

	if flyby_observation_num is None and flyby_id is None:
		logger.critical("\nCRITICAL ERROR: Requires either a flyby_observation_num OR flyby_id.\nAvaliable flyby_observation_num: {0}\nAvaliable flyby_id: {1}".format(avaliable_flyby_id, avaliable_observation_numbers))
		exit()

	if flyby_id is not None:
		if type(flyby_id) != str:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(type(flyby_id)))
			exit()
		if flyby_id not in avaliable_flyby_id:
			logger.critical("\nCRITICAL ERROR, [flyby_id]: '{0}' not in avaliable ids options '{1}'".format(flyby_id, avaliable_flyby_id))
			exit()

	if flyby_observation_num is not None:
		if type(flyby_observation_num) != str:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(type(flyby_observation_num)))
			exit()
		if flyby_observation_num not in avaliable_observation_numbers:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: '{0}' not in avaliable observation options '{1}'".format(flyby_observation_num, avaliable_observation_numbers))
			exit()

	segement_options = ['S01', 'S02', 'S03']
	if segment_num is None:
		logger.critical("\nCRITICAL ERROR, [segment_num]: segment_num number required out of avaliable options {0}, none given".format(segement_options))
		exit()
	if type(segment_num) != str:
		logger.critical("\nCRITICAL ERROR, [segment_num]: Must be a str, current type = '{0}'".format(type(segment_num)))
		exit()
	if segment_num not in segement_options:
		logger.critical("\nCRITICAL ERROR, [segment_num]: '{0}' not an avaliable segment option '{1}'".format(segment_num, segement_options))
		exit()

	if len(additional_data_types_to_download) != 0:
		if type(additional_data_types_to_download) != list:
			logger.critical("\nCRITICAL ERROR [additional_data_types_to_download]: Must be a list, current type = '{0}'".format(type(additional_data_types_to_download)))
			exit()
		for data_type in additional_data_types_to_download:
			if type(data_type) != str:
				logger.critical("\nCRITICAL ERROR [additional_data_types_to_download]: All data types should be strings, but '{0}' current type = '{0}'".format(data_type, type(data_type)))

		# Get data types for the coradr type from coradr_jpl_options.csv
		coradr_data_types_available = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
		df = pd.read_csv(coradr_data_types_available)
		if flyby_id is not None: 
			flyby_observation_num = pydar.convertFlybyIDToObservationNumber(flyby_id)
		coradr_versions = df[df['CORADR ID'].str.contains(flyby_observation_num)]
		version_id = ""
		if len(coradr_versions) > 1:
			for i in range(len(coradr_versions)):
				version_id = "_V0{0}".format(i+1)
		coradr_id = "CORADR_{0}{1}".format(flyby_observation_num, version_id)
		coradr_row = df.loc[df['CORADR ID'] == coradr_id]
		coradr_data_types = []
		for index, row in coradr_row.iterrows():
			row = row.tolist()
		for i, row_bool in enumerate(row[2:]): # Ignores first two columns: CORADR ID and Is Titan Flyby
			if row_bool is True:
				coradr_data_types.append(pydar.datafile_types_columns[i])

		for data_type in additional_data_types_to_download:
			if data_type not in coradr_data_types:
				logger.critical("\nCRITICAL ERROR [additional_data_types_to_download]: Data type '{0}' not avaliable in {1}".format(data_type, coradr_data_types))
				exit()

	if resolution is not None and top_x_resolutions is not None:
		logger.critical("\nCRITICAL ERROR: Requires either a resolution OR a top_x_resolutions, not both".format(type(resolution)))
		exit()

	if resolution is not None :
		if type(resolution) != str:
			logger.critical("\nCRITICAL ERROR, [resolution]: Must be a str, current type = '{0}'".format(type(resolution)))
			exit()
		if resolution not in pydar.resolution_types:
			logger.critical("\nCRITICAL ERROR, [resolution]: resolution '{0}' must be a valid resolution type in {1}".format(resolution, pydar.resolution_types))
			exit()

	if top_x_resolutions is not None:
		if type(top_x_resolutions) != int:
			logger.critical("\nCRITICAL ERROR, [top_x_resolutions]: Must be a int, current type = '{0}'".format(type(top_x_resolutions)))
			exit()
		if top_x_resolutions < 1 or top_x_resolutions > 5:
			logger.critical("\nCRITICAL ERROR, [top_x_resolutions]: Must be a value from 1 to 5, not '{0}'".format(top_x_resolutions))
			exit()

def errorHandlingConvertFlybyIDToObservationNumber(flyby_id=None):
	# Error Handling for Converting a Flyby ID into an Observation Number
	if type(flyby_id) != str:
		logger.critical("\nCRITICAL ERROR, [flyby_id]: Must be a str, current type = '{0}'".format(type(flyby_id)))
		exit()

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	valid_flyby_ids = []
	flyby_id_found = False
	for index, row in flyby_dataframe.iterrows():
		valid_flyby_ids.append(row[0])
		if row[0] == flyby_id:
			flyby_id_found = True
			break
	if not flyby_id_found:
		logger.critical("\nCRITICAL ERROR, [flyby_id]: Invalid flyby_id, '{0}', choose from:\n{1}".format(flyby_id, valid_flyby_ids))
		exit()

def errorHandlingConvertObservationNumberToFlybyID(flyby_observation_num=None):
	# Error Handling for Converting an Observation Number to a Flyby ID
	if type(flyby_observation_num) != str:
		logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(type(flyby_observation_num)))
		exit()

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	valid_observation_nums = []
	observation_num_found = False
	for index, row in flyby_dataframe.iterrows():
		take_ob_num = "0" + row[1].split(" ")[1]
		valid_observation_nums.append(take_ob_num)
		if take_ob_num == flyby_observation_num:
			observation_num_found = True
			break
	if not observation_num_found:
		logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Invalid flyby_observation_num, '{0}', choose from:\n{1}".format(flyby_observation_num, valid_observation_nums))
		exit()

def errorHandlingDisplayImages(image_directory=None):
	# Error Handling for Displaying Images from an Image Directory
	if type(image_directory) != str:
		logger.critical("\nCRITICAL ERROR, [image_directory]: Must be a str, current type = '{0}'".format(type(image_directory)))
		exit()

def errorHandlingREADME(coradr_results_directory=None,
						section_to_print=None,
						print_to_console=True):
	if type(coradr_results_directory) != str:
		logger.critical("\nCRITICAL ERROR, [coradr_results_directory]: Must be a str, current type = '{0}'".format(type(coradr_results_directory)))
		exit()

	if type(section_to_print) != str:
		logger.critical("\nCRITICAL ERROR, [section_to_print]: Must be a str, current type = '{0}'".format(type(section_to_print)))
		exit()

	if type(print_to_console) != bool:
		logger.critical("\nCRITICAL ERROR, [print_to_console]: Must be a bool, current type = '{0}'".format(type(print_to_console)))
		exit()

def errorHandlingRetrieveIDSByFeature(feature_name=None):
	if type(feature_name) != str:
		logger.critical("\nCRITICAL ERROR, [feature_name]: Must be a str, current type = '{0}'".format(type(feature_name)))
		exit()

def errorHandlingRetrieveByLatitudeLongitude(latitude=None,
											longitude=None):
	if type(latitude) != float and type(latitude) != int:
		logger.critical("\nCRITICAL ERROR, [latitude]: Must be a float or int, current type = '{0}'".format(type(latitude)))
		exit()

	if latitude > 90 or latitude < -90:
		logger.critical("\nCRITICAL ERROR, [latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(latitude))
		exit()

	if type(longitude) != float and type(longitude) != int:
		logger.critical("\nCRITICAL ERROR, [longitude]: Must be a float or int, current type = '{0}'".format(type(longitude)))
		exit()

	if longitude < 0 or longitude > 360:
		logger.critical("\nCRITICAL ERROR, [longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(longitude))
		exit()

def errorHandlingRetrieveByLatitudeLongitudeRange(northernmost_latitude=None,
												southernmost_latitude=None,
												easternmost_longitude=None,
												westernmost_longitude=None):
	if type(northernmost_latitude) != float and type(northernmost_latitude) != int:
		logger.critical("\nCRITICAL ERROR, [northernmost_latitude]: Must be a float or int, current type = '{0}'".format(type(northernmost_latitude)))
		exit()

	if type(southernmost_latitude) != float and type(southernmost_latitude) != int:
		logger.critical("\nCRITICAL ERROR, [southernmost_latitude]: Must be a float or int, current type = '{0}'".format(type(southernmost_latitude)))
		exit()

	if northernmost_latitude > 90 or northernmost_latitude < -90:
		logger.critical("\nCRITICAL ERROR, [northernmost_latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(northernmost_latitude))
		exit()

	if southernmost_latitude > 90 or southernmost_latitude < -90:
		logger.critical("\nCRITICAL ERROR, [southernmost_latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(southernmost_latitude))
		exit()

	if type(easternmost_longitude) != float and type(easternmost_longitude) != int:
		logger.critical("\nCRITICAL ERROR, [easternmost_longitude]: Must be a float or int, current type = '{0}'".format(type(easternmost_longitude)))
		exit()

	if type(westernmost_longitude) != float and type(westernmost_longitude) != int:
		logger.critical("\nCRITICAL ERROR, [westernmost_longitude]: Must be a float or int, current type = '{0}'".format(type(westernmost_longitude)))
		exit()

	if easternmost_longitude < 0 or easternmost_longitude > 360:
		logger.critical("\nCRITICAL ERROR, [easternmost_longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(easternmost_longitude))
		exit()

	if westernmost_longitude < 0 or westernmost_longitude > 360:
		logger.critical("\nCRITICAL ERROR, [westernmost_longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(westernmost_longitude))
		exit()

	if northernmost_latitude < southernmost_latitude:
		logger.critical("\nCRITICAL ERROR, [latitude]: northernmost_latitude must be greater than southernmost_latitude")
		exit()

	if westernmost_longitude > easternmost_longitude:
		logger.critical("\nCRITICAL ERROR, [longitude]: westernmost_longitude must be less than easternmost_longitude")
		exit()


def errorHandlingRetrieveIDSByTime(year=None, doy=None, hour=None, minute=None, second=None, millisecond=None):
	if year == None:
		logger.critical("\nCRITICAL ERROR, [year]: year is required")
		exit()
	if type(year) != int:
		logger.critical("\nCRITICAL ERROR, [year]: Must be an int, current type = '{0}'".format(type(year)))
		exit()
	if year < 2004 or year > 2014:
		logger.critical("\nCRITICAL ERROR, [year]: year must be between 2004-2014")
		exit()

	if doy == None:
		logger.critical("\nCRITICAL ERROR, [doy]: doy is required")
		exit()
	if type(doy) != int:
		logger.critical("\nCRITICAL ERROR, [doy]: Must be an int, current type = '{0}'".format(type(doy)))
		exit()
	if doy < 0 or doy > 365:
		logger.critical("\nCRITICAL ERROR, [doy]: doy must be between 0-365")
		exit()

	if hour is not None:
		if type(hour) != int:
			logger.critical("\nCRITICAL ERROR, [hour]: Must be an int, current type = '{0}'".format(type(hour)))
			exit()
		if hour < 0 or hour > 23:
			logger.critical("\nCRITICAL ERROR, [hour]: hour must be within UTC range between 0 to 23")
			exit()

	if minute is not None:
		if type(minute) != int:
			logger.critical("\nCRITICAL ERROR, [minute]: Must be an int, current type = '{0}'".format(type(minute)))
			exit()
		if minute < 0 or minute > 59:
			logger.critical("\nCRITICAL ERROR, [minute]: minute must be within range between 0 to 59")
			exit()

	if second is not None:
		if type(second) != int:
			logger.critical("\nCRITICAL ERROR, [second]: Must be an int, current type = '{0}'".format(type(second)))
			exit()
		if second < 0 or second > 59:
			logger.critical("\nCRITICAL ERROR, [second]: second must be within range between 0 to 59")
			exit()

	if millisecond is not None:
		if type(millisecond) != int:
			logger.critical("\nCRITICAL ERROR, [millisecond]: Must be an int, current type = '{0}'".format(type(millisecond)))
			exit()
		if millisecond < 0 or millisecond > 999:
			logger.critical("\nCRITICAL ERROR, [millisecond]: second must be a postive value from 0 to 999")
			exit()

def errorHandlingRetrieveIDSByTimeRange(start_year=None, 
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

	if start_year is None:
		logger.critical("\nCRITICAL ERROR, [start_year]: start_year is required")
		exit()
	if start_doy is None:
		logger.critical("\nCRITICAL ERROR, [start_doy]: start_doy is required")
		exit()

	if end_year is None:
		logger.critical("\nCRITICAL ERROR, [end_year]: end_year is required")
		exit()
	if end_doy is None:
		logger.critical("\nCRITICAL ERROR, [end_doy]: end_doy is required")
		exit()

	errorHandlingRetrieveIDSByTime(year=start_year, doy=start_doy, hour=start_hour, minute=start_minute, second=start_second, millisecond=start_millisecond)
	errorHandlingRetrieveIDSByTime(year=end_year, doy=end_doy, hour=end_hour, minute=end_minute, second=end_second, millisecond=end_millisecond)

	if start_year > end_year:
		logger.critical("\nCRITICAL ERROR, [year]: start_year must be less than/equal to end_year")
		exit()

	if start_year != end_year:
		return
	if start_doy is not None and end_doy is not None:
		if start_doy > end_doy:
			logger.critical("\nCRITICAL ERROR, [doy]: start_doy must be less than/equal to end_doy")
			exit()
		if start_doy != end_doy:
			return
		if start_hour is not None and end_hour is not None:
			if start_hour > end_hour:
				logger.critical("\nCRITICAL ERROR, [hour]: start_hour must be less than/equal to end_hour")
				exit()
		if start_hour != end_hour:
			return
		if start_minute is not None and end_minute is not None:
			if start_minute > end_minute:
				logger.critical("\nCRITICAL ERROR, [minute]: start_minute must be less than/equal to end_minute")
				exit()
		if start_minute != end_minute:
			return
		if start_second is not None and end_second is not None:
			if start_second > end_second:
				logger.critical("\nCRITICAL ERROR, [second]: start_second must be less than/equal to end_second")
				exit()
			if start_second != end_second:
				return
			if start_millisecond is not None and end_millisecond is not None:
				if start_millisecond > end_millisecond:
					logger.critical("\nCRITICAL ERROR, [millisecond]: start_millisecond must be less than/equal to end_millisecond")
					exit()

def errorHandlingSbdrMakeShapeFile(filename=None, 
									fields=[],
									write_files=False,
									saronly=0, 
									usepassive=False, 
									ind=None, 
									file_out=[], 
									lon360=False):
	logger.critical("TODO: errorHandlingSbdrMakeShapeFile")

	if type(filename) != str:
		logger.critical("\nCRITICAL ERROR, [filename]: Must be an str, current type = '{0}'".format(type(filename)))
		exit()

	if type(fields) != list:
		logger.critical("\nCRITICAL ERROR, [fields]: Must be an list, current type = '{0}'".format(type(fields)))
		exit()

	if len(fields) != 0:
		for field_item in fields:
			if field_item not in pydar.field_options:
				logger.critical("\nCRITICAL ERROR, [fields]: Must be a valid option, not '{0}', chose from {1}".format(field_item, pydar.field_options))
				exit()

	if type(saronly) != int:
		logger.critical("\nCRITICAL ERROR, [saronly]: Must be an int, current type = '{0}'".format(type(saronly)))
		exit()

	if saronly not in [0, 1, 2, 3]:
		logger.critical("\nCRITICAL ERROR, [saronly]: Must be a valid option, not '{0}', chose from {1}".format(saronly, [0, 1, 2, 3]))
		exit()

	if type(lon360) != bool:
		logger.critical("\nCRITICAL ERROR, [lon360]: Must be an bool, current type = '{0}'".format(type(lon360)))
		exit()
