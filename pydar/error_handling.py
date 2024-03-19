########################################################################
# ERROR CATCHES AND LOGGING FOR CLARITY WHEN USING PYDAR
########################################################################

# Built in Python functions
import logging
import os
import csv

# External Python libraries (installed via pip install)
import pandas as pd

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

def errorHandlingExtractFlybyDataImages(flyby_observation_num=None,
										flyby_id=None,
										segment_num=None,
										additional_data_types_to_download=[],
										resolution=None,
										top_x_resolutions=None):
	# Error Handling for extract_flyby_parameters variables: extractFlybyDataImages()
	available_flyby_id, available_observation_numbers = pydar.getFlybyData()

	if flyby_observation_num is None and flyby_id is None:
		raise ValueError(f"Requires either a flyby_observation_num OR flyby_id.\nAvailable flyby_observation_num: {available_flyby_id}\nAvailable flyby_id: {available_observation_numbers}")

	if flyby_observation_num is not None and flyby_id is not None:
		raise ValueError("Requires either a flyby_observation_num OR flyby_id, not both.")

	if flyby_id is not None:
		if type(flyby_id) != str:
			raise ValueError(f"[flyby_id]: Must be a str, current type = '{type(flyby_id)}'")
		if flyby_id not in available_flyby_id:
			raise ValueError(f"[flyby_id]: '{flyby_id}' not in available ids options '{available_flyby_id}'")

	if flyby_observation_num is not None:
		if type(flyby_observation_num) != str:
			raise ValueError(f"[flyby_observation_num]: Must be a str, current type = '{type(flyby_observation_num)}'")
		if flyby_observation_num not in available_observation_numbers:
			raise ValueError(f"[flyby_observation_num]: '{flyby_observation_num}' not in available observation options '{available_observation_numbers}'")

	segment_options = ['S01', 'S02', 'S03', 'S04']
	if segment_num is None:
		raise ValueError(f"[segment_num]: segment_num number required out of available options {segment_options}, none given")
	if type(segment_num) != str:
		raise ValueError(f"[segment_num]: Must be a str, current type = '{type(segment_num)}'")
	if segment_num not in segment_options:
		raise ValueError(f"[segment_num]: '{segment_num}' not an available segment option '{segment_options}'")

	if len(additional_data_types_to_download) != 0:
		raise ValueError("\nINFO [additional_data_types_to_download]: Current v1 behavior does not support additional_data_types_to_download, so no additional files will be included in the download")
		"""
		if type(additional_data_types_to_download) != list:
			print("\nCRITICAL ERROR [additional_data_types_to_download]: Must be a list, current type = '{0}'".format(type(additional_data_types_to_download)))
			exit()
		for data_type in additional_data_types_to_download:
			if type(data_type) != str:
				print("\nCRITICAL ERROR [additional_data_types_to_download]: All data types should be strings, but '{0}' current type = '{0}'".format(data_type, type(data_type)))

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
				print("\nCRITICAL ERROR [additional_data_types_to_download]: Data type '{0}' not available in {1}".format(data_type, coradr_data_types))
				exit()
		"""

	if resolution is not None :
		if type(resolution) != str:
			raise ValueError(f"[resolution]: Must be a str, current type = '{type(resolution)}'")
		if resolution not in pydar.resolution_types:
			raise ValueError(f"[resolution]: resolution '{resolution}' must be a valid resolution type in {pydar.resolution_types}")

	if top_x_resolutions is not None:
		if type(top_x_resolutions) != int:
			raise ValueError(f"[top_x_resolutions]: Must be a int, current type = '{type(top_x_resolutions)}'")
		if top_x_resolutions < 1 or top_x_resolutions > 5:
			raise ValueError(f"[top_x_resolutions]: Must be a value from 1 to 5, not '{top_x_resolutions}'")

def errorHandlingConvertFlybyIDToObservationNumber(flyby_id=None):
	# Error Handling for Converting a Flyby ID into an Observation Number: convertFlybyIDToObservationNumber()
	if flyby_id is None:
		raise ValueError("[flyby_id]: A valid flyby_id string is required")

	if type(flyby_id) != str:
		raise ValueError(f"[flyby_id]: Must be a str, current type = '{type(flyby_id)}'")

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	valid_flyby_ids = []
	flyby_id_found = False
	for index, row in flyby_dataframe.iterrows():
		valid_flyby_ids.append(row.iloc[0])
		if row.iloc[0] == flyby_id:
			flyby_id_found = True
			break
	if not flyby_id_found:
		raise ValueError(f"[flyby_id]: Invalid flyby_id, '{flyby_id}', choose from:\n{valid_flyby_ids}")

def errorHandlingConvertObservationNumberToFlybyID(flyby_observation_num=None):
	# Error Handling for Converting an Observation Number to a Flyby ID: convertObservationNumberToFlybyID()
	if flyby_observation_num is None:
		raise ValueError("[flyby_observation_num]: A valid flyby_observation_num string is required")

	if type(flyby_observation_num) != str:
		raise ValueError(f"[flyby_observation_num]: Must be a str, current type = '{type(flyby_observation_num)}'")

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	valid_observation_nums = []
	observation_num_found = False
	for index, row in flyby_dataframe.iterrows():
		take_ob_num = "0" + row.iloc[1].split(" ")[1]
		valid_observation_nums.append(take_ob_num)
		if take_ob_num == flyby_observation_num:
			observation_num_found = True
			break
	if not observation_num_found:
		raise ValueError(f"[flyby_observation_num]: Invalid flyby_observation_num, '{flyby_observation_num}', choose from:\n{valid_observation_nums}")

def errorHandlingDisplayImages(image_directory=None, fig_title=None, cmap=None, figsize_n=None, fig_dpi=None):
	# Error Handling for Displaying Images from an Image Directory: displayImages()
	if image_directory == None:
		raise ValueError("[image_directory]: image_directory is required")
	else:
		if type(image_directory) != str:
			raise ValueError(f"[image_directory]: Must be a str, current type = '{type(image_directory)}'")

	if fig_title is not None and type(fig_title) != str:
		raise ValueError(f"[fig_title]: Must be a str, current type = '{type(fig_title)}'")

	if cmap is not None and type(cmap) != str:
		raise ValueError(f"[cmap]: Must be a str, current type = '{type(cmap)}'")

	if type(figsize_n) != int:
		raise ValueError(f"[figsize_n]: Must be a int, current type = '{type(figsize_n)}'")
	else:
		if figsize_n < 1:
			raise ValueError(f"[figsize_n]: figsize_n must be greater than 1, current value = '{figsize_n}'")

	if type(fig_dpi) != int:
		raise ValueError(f"[fig_dpi]: Must be a int, current type = '{type(fig_dpi)}'")
	else:
		if fig_dpi < 1:
			raise ValueError(f"[fig_dpi]: fig_dpi must be greater than 1, current value = '{fig_dpi}'")

def errorHandlingREADME(coradr_results_directory=None,
						section_to_print=None,
						print_to_console=True):
	# Error Handling for README options: read_readme
	if coradr_results_directory is None:
		raise ValueError("[coradr_results_directory]: coradr_results_directory is required")
	else:
		if type(coradr_results_directory) != str:
			raise ValueError(f"[coradr_results_directory]: Must be a str, current type = '{type(coradr_results_directory)}'")

	if section_to_print is not None and type(section_to_print) != str:
		raise ValueError(f"[section_to_print]: Must be a str, current type = '{type(section_to_print)}'")

	if type(print_to_console) != bool:
		raise ValueError(f"[print_to_console]: Must be a bool, current type = '{type(print_to_console)}'")

def errorHandlingRetrieveIDSByFeature(feature_name=None):
	# Error Handling for retrieving the IDs for a specific feature name: retrieveIDSByFeature()
	if feature_name is None:
		raise ValueError("[feature_name]: feature_name is required")
	else:
		if type(feature_name) != str:
			raise ValueError(f"[feature_name]: Must be a str, current type = '{type(feature_name)}'")

def errorHandlingRetrieveIDSByLatitudeLongitude(latitude=None,
												longitude=None):
	# Error Handling for retrieving IDs based on latitude and longitude

	if latitude is None:
		raise ValueError("[latitude]: latitude is required")

	if type(latitude) != float and type(latitude) != int:
		raise ValueError(f"[latitude]: Must be a float or int, current type = '{type(latitude)}'")

	if latitude > 90 or latitude < -90:
		raise ValueError(f"[latitude]: Latitude must be between 90 and -90, current value = '{latitude}'")

	if longitude is None:
		raise ValueError("[longitude]: longitude is required")
	if type(longitude) != float and type(longitude) != int:
		raise ValueError(f"[longitude]: Must be a float or int, current type = '{type(longitude)}'")

	if longitude < 0 or longitude > 360:
		raise ValueError(f"[longitude]: Longitude must be between 0 and 360, current value = '{longitude}'")

def errorHandlingRetrieveIDSByLatitudeLongitudeRange(min_latitude=None,
													max_latitude=None,
													min_longitude=None,
													max_longitude=None):
	# Error Handling for retrieving IDs based on a range of latitude and longitudes
	if min_latitude is None:
		raise ValueError("[min_latitude]: min_latitude is required")
	else:
		if type(min_latitude) != float and type(min_latitude) != int:
			raise ValueError(f"[min_latitude]: Must be a float or int, current type = '{type(min_latitude)}'")

	if max_latitude is None:
		raise ValueError("[max_latitude]: max_latitude is required")
	else:
		if type(max_latitude) != float and type(max_latitude) != int:
			raise ValueError(f"[max_latitude]: Must be a float or int, current type = '{type(max_latitude)}'")

	if min_latitude > 90 or min_latitude < -90:
		raise ValueError(f"[min_latitude]: Latitude must be between 90 and -90, current value = '{min_latitude}'")

	if max_latitude > 90 or max_latitude < -90:
		raise ValueError(f"[max_latitude]: Latitude must be between 90 and -90, current value = '{max_latitude}'")

	if min_longitude is None:
		raise ValueError("[min_longitude]: min_longitude is required")
	else:
		if type(min_longitude) != float and type(min_longitude) != int:
			raise ValueError(f"[min_longitude]: Must be a float or int, current type = '{type(min_longitude)}'")

	if max_longitude is None:
		raise ValueError("[max_longitude]: max_longitude is required")
	else:
		if type(max_longitude) != float and type(max_longitude) != int:
			raise ValueError(f"[max_longitude]: Must be a float or int, current type = '{type(max_longitude)}'")

	if min_longitude < 0 or min_longitude > 360:
		raise ValueError(f"[min_longitude]: Longitude must be between 0 and 360, current value = '{min_longitude}'")

	if max_longitude < 0 or max_longitude > 360:
		raise ValueError(f"[max_longitude]: Longitude must be between 0 and 360, current value = '{max_longitude}'")

	if max_latitude < min_latitude:
		raise ValueError("[latitude]: max_latitude must be greater than min_latitude")

	if max_longitude < min_longitude:
		raise ValueError("[longitude]: max_longitude must be greater than min_longtiude")


def errorHandlingRetrieveIDSByTime(year=None, doy=None, hour=None, minute=None, second=None, millisecond=None):
	# Error handling for retrieving IDs based on a specific time
	if year is None:
		raise ValueError("[year]: year is required")
	else:
		if type(year) != int:
			raise ValueError(f"[year]: Must be an int, current type = '{type(year)}'")
		if year < 2004 or year > 2014:
			raise ValueError("[year]: year must be between 2004-2014")

	if doy is None:
		raise ValueError("[doy]: doy is required")
	else:
		if type(doy) != int:
			raise ValueError(f"[doy]: Must be an int, current type = '{type(doy)}'")
		if doy < 0 or doy > 365:
			raise ValueError("[doy]: doy must be between 0-365")

	if hour is not None:
		if type(hour) != int:
			raise ValueError(f"[hour]: Must be an int, current type = '{type(hour)}'")
		if hour < 0 or hour > 23:
			raise ValueError("[hour]: hour must be within UTC range between 0 to 23")

	if minute is not None:
		if type(minute) != int:
			raise ValueError(f"[minute]: Must be an int, current type = '{type(minute)}'")
		if minute < 0 or minute > 59:
			raise ValueError("[minute]: minute must be within range between 0 to 59")

	if second is not None:
		if type(second) != int:
			raise ValueError(f"[second]: Must be an int, current type = '{type(second)}'")
		if second < 0 or second > 59:
			raise ValueError("[second]: second must be within range between 0 to 59")

	if millisecond is not None:
		if type(millisecond) != int:
			raise ValueError(f"[millisecond]: Must be an int, current type = '{type(millisecond)}'")
		if millisecond < 0 or millisecond > 999:
			raise ValueError("[millisecond]: second must be a positive value from 0 to 999")

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
	# Error handling for retrieving IDs based on a range of times
	if start_year is None:
		raise ValueError("[start_year]: start_year is required")
	if start_doy is None:
		raise ValueError("[start_doy]: start_doy is required")

	if end_year is None:
		raise ValueError("[end_year]: end_year is required")
	if end_doy is None:
		raise ValueError("[end_doy]: end_doy is required")

	errorHandlingRetrieveIDSByTime(year=start_year, doy=start_doy, hour=start_hour, minute=start_minute, second=start_second, millisecond=start_millisecond)
	errorHandlingRetrieveIDSByTime(year=end_year, doy=end_doy, hour=end_hour, minute=end_minute, second=end_second, millisecond=end_millisecond)

	if start_year > end_year:
		raise ValueError("[year]: start_year must be less than/equal to end_year")

	if start_year != end_year:
		return
	if start_doy is not None and end_doy is not None:
		if start_doy > end_doy:
			raise ValueError("[doy]: start_doy must be less than/equal to end_doy")
		if start_doy != end_doy:
			return
		if start_hour is not None and end_hour is not None:
			if start_hour > end_hour:
				raise ValueError("[hour]: start_hour must be less than/equal to end_hour")
		if start_hour != end_hour:
			return
		if start_minute is not None and end_minute is not None:
			if start_minute > end_minute:
				raise ValueError("[minute]: start_minute must be less than/equal to end_minute")
		if start_minute != end_minute:
			return
		if start_second is not None and end_second is not None:
			if start_second > end_second:
				raise ValueError("[second]: start_second must be less than/equal to end_second")
			if start_second != end_second:
				return
			if start_millisecond is not None and end_millisecond is not None:
				if start_millisecond > end_millisecond:
					raise ValueError("[millisecond]: start_millisecond must be less than/equal to end_millisecond")

def errorHandlingSbdrMakeShapeFile(filename=None, 
									fields=[],
									write_files=False,
									saronly=0, 
									usepassive=False, 
									ind=None, 
									file_out=None, 
									lon360=False):
	# Error handling for using SBDR to make a shapefile
	if type(filename) != str:
		raise ValueError(f"[filename]: Must be an str, current type = '{type(filename)}'")

	valid_file_extensions = ["sbdr", "lbdr", "tab"]
	if filename.split(".")[1].lower() not in valid_file_extensions:
		raise ValueError(f"[filename]: Unrecognized Data File Format '{filename.split('.')[1]}', must be within '{valid_file_extensions}'")

	if type(fields) != list:
		raise ValueError(f"[fields]: Must be an list, current type = '{type(fields)}'")

	if len(fields) != 0:
		for field_item in fields:
			if field_item not in pydar.field_options:
				raise ValueError(f"[fields]: Must be a valid option, not '{field_item}', chose from {pydar.field_options}")

	if type(saronly) != int:
		raise ValueError(f"[saronly]: Must be an int, current type = '{type(saronly)}'")

	if saronly not in [0, 1, 2, 3]:
		raise ValueError(f"[saronly]: Must be a valid option, not '{saronly}', chose from [0, 1, 2, 3]")

	if file_out is not None and type(file_out) != str:
		raise ValueError(f"[file_out]: Must be an str, current type = '{type(file_out)}'")

	if type(lon360) != bool:
		raise ValueError(f"[lon360]: Must be an bool, current type = '{type(lon360)}'")
