# Extract flyby parameters from CASSINI
import zipfile
import os
from datetime import datetime, timedelta

import pandas as pd
import logging
from urllib import request, error
from bs4 import BeautifulSoup

import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

resolution_types = ["B", "D", "F", "H", "I"] # 2, 8, 32, 128, 256 pixels/degree
datafile_types_columns = ["ABDR", "ASUM", "BIDR", "LBDR", "SBDR", "STDR"]

def getFlybyData():
	# Header: Titan flyby id, Radar Data Take Number, Sequence number, Orbit Number/ID
	flyby_id = []
	flyby_radar_take_num = []
	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		row = row.tolist()
		flyby_id.append(row[0])
		radar_take_num = row[1].split(" ")[1]
		while len(radar_take_num) < 4:
			radar_take_num = "0" + radar_take_num # set all radar take numbers to be four digits long: 229 -> 0229
		flyby_radar_take_num.append(radar_take_num)
	# returns a list of flyby IDs and associated Radar Data Take Number
	return flyby_id, flyby_radar_take_num

def convertFlybyIDToObservationNumber(flyby_id=None):
	# convert Flyby ID to Observation Number to find data files
	pydar.errorHandlingConvertFlybyIDToObservationNumber(flyby_id=flyby_id)

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		if row[0] == flyby_id:
			observation_number = row[1].split(" ")[1]
			while len(observation_number) < 4:
				observation_number = "0" + observation_number # set all radar take numbers to be four digits long: 229 -> 0229
			return observation_number

def convertObservationNumberToFlybyID(flyby_observation_num=None):
	# convert Flyby ID to Observation Number to find data files
	pydar.errorHandlingConvertObservationNumberToFlybyID(flyby_observation_num=flyby_observation_num)

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		take_ob_num = "0" + row[1].split(" ")[1]
		if take_ob_num == flyby_observation_num:
			return row[0] # returns flyby ID

def retrieveJPLCoradrOptions(flyby_observiation_num):
	# Read JPL Options from CSV
	jpl_coradr_options = []
	coradr_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
	coradr_dataframe = pd.read_csv(coradr_csv_file)
	for index, row in coradr_dataframe.iterrows():
		row = row.tolist()
		jpl_coradr_options.append(row[0])

	find_cordar_listing = 'CORADR_{0}'.format(flyby_observiation_num)
	version_types_avaliable = list(filter(lambda x: find_cordar_listing in x, jpl_coradr_options))
	more_accurate_model_number = version_types_avaliable[-1] # always choose the last and more up to date version number
	logger.info("Most recent CORADR version is {0} from the available list {1}".format(more_accurate_model_number, version_types_avaliable))
	return more_accurate_model_number

def downloadAAREADME(cordar_file_name, segment_id):
	# Download AAREADME.txt within a CORADR directory
	aareadme_name = "AAREADME.TXT"
	aareadme_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/{1}".format(cordar_file_name, aareadme_name)

	# Retrieve a list of all elements from the base URL to download AAREADME.txt
	logger.info("Retrieving {0} {1}".format(cordar_file_name, aareadme_name))
	aareadme_name = os.path.join("pydar_results/{0}_{1}".format(cordar_file_name, segment_id), aareadme_name)
	try:
		request.urlretrieve(aareadme_url)
	except error.HTTPError as err:
		logger.critical("Unable to access: {0}\nError (and exiting): '{1}'".format(aareadme_url, err.code))
		exit()
	else:
		response = request.urlretrieve(aareadme_url, aareadme_name)

def downloadBIDRCORADRData(cordar_file_name, segment_id, resolution_px):
	# Download BDIR files
	base_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/".format(cordar_file_name)
	logger.info("Retrieving BIDR filenames from: {0}\n".format(base_url))

	# Retrieve a list of all elements from the base URL to download
	base_html = request.urlopen(base_url).read()
	soup = BeautifulSoup(base_html, 'html.parser')
	table = soup.find('table', {"id": "indexlist"})
	table_text = (table.text).split("\n")
	url_filenames = []
	all_bidr_files = []
	for txt in table_text:
		if txt.startswith('BI'):
			filename = (txt.split('/')[0]).split(".")[0]
			if 'LBL' in (txt.split('/')[0]).split(".")[1]:
				filename += '.LBL'
			if 'ZIP' in (txt.split('/')[0]).split(".")[1]:
				filename += '.ZIP'
			all_bidr_files.append(filename)
			if segment_id in filename: # only save certain segements
				for resolution in resolution_px: # only save top x resolutions
					bi_types = ["B", "E", "T", "N", "M", "L"] # BI<OPTION>Q<RESOLUTION>
					for bi in bi_types:
						if "BI{0}Q{1}".format(bi, resolution) in filename:
							url_filenames.append(filename)

	logger.info("All BIDR files found with specified resolution, segment, and flyby identification: {0}\n".format(url_filenames))
	if len(url_filenames) == 0:
		logger.critical("No BIDR files found with resolution, segment, and flyby identification. Please use different parameters to retrieve data.\nAll files found: {0}".format(all_bidr_files))
		exit()

	for i, coradr_file in enumerate(url_filenames):
		if 'LBL' in coradr_file:
			label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(cordar_file_name, coradr_file)
			logger.info("Retrieving [{0}/{1}]: {2}".format(i+1, len(url_filenames), label_url))
			label_name = label_url.split("/")[-1].split(".")[0] + ".LBL"
			label_name = os.path.join("pydar_results/{0}_{1}".format(cordar_file_name, segment_id), label_name)
			try:
				request.urlretrieve(label_url)
			except error.HTTPError as err:
				logger.critical("Unable to access: {0}\nError (and exiting): '{1}'".format(label_url, err.code))
				exit()
			else:
				response = request.urlretrieve(label_url, label_name)
		if 'ZIP' in coradr_file:
			data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(cordar_file_name, coradr_file)
			logger.info("Retrieving [{0}/{1}]: {2}".format(i+1, len(url_filenames), data_url))
			zipfile_name = data_url.split("/")[-1].split(".")[0] + ".zip"
			zipfile_name = os.path.join("pydar_results/{0}_{1}".format(cordar_file_name, segment_id), zipfile_name)
			try:
				request.urlretrieve(data_url)
			except error.HTTPError as err:
				logger.info("Unable to access: {0}\nError (and exiting): '{1}'".format(data_url, err.code))
				exit()
			else:
				response = request.urlretrieve(data_url, zipfile_name)
				zipped_image = zipfile_name.split(".")[0] + ".IMG"
				with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
					zipped_image_path = os.path.join("pydar_results/{0}_{1}".format(cordar_file_name, segment_id))
					zip_ref.extractall(zipped_image_path)

def downloadSBDRCORADRData(cordar_file_name, segment_id):
	# Download SBDR files
	base_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/SBDR/".format(cordar_file_name)
	logger.info("\nRetrieving SBDR filenames from: {0}".format(base_url))

	# Retrieve a SBDR file from filename at SBDR URL
	base_html = request.urlopen(base_url).read()
	soup = BeautifulSoup(base_html, 'html.parser')
	table = soup.find('table', {"id": "indexlist"})
	table_text = (table.text).split("\n")
	sbdr_files = []
	sbdr_filename = ''
	for txt in table_text:
		if txt.startswith('SBDR'):
			sbdr_filename = (txt.split('/')[0]).split(".")[0]
			if 'TAB' in (txt.split('/')[0]).split(".")[1]: # TAB information
				sbdr_filename += '.TAB'
			if 'FMT' in (txt.split('/')[0]).split(".")[1]: # FMT information required to read TAB
				sbdr_filename += '.FMT'
			sbdr_files.append(sbdr_filename)

	logger.info("SBDR files found: {0}".format(sbdr_files))
	if len(sbdr_files) == 0:
		logger.critical("No SBDR files were found with resolution, segment, and flyby identification. Please use different parameters to retrieve data")
		exit()

	for sbdr_file in sbdr_files:
		sbdr_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/SBDR/{1}".format(cordar_file_name, sbdr_file)
		logger.info("Retrieving SBDR file '{0}': {1}".format(sbdr_file, sbdr_url))
		sbdr_name = os.path.join("pydar_results/{0}_{1}".format(cordar_file_name, segment_id), sbdr_file)
		try:
			request.urlretrieve(sbdr_url)
		except error.HTTPError as err:
			logger.critical("Unable to access: {0}\nError (and exiting): '{1}'".format(sbdr_url, err.code))
			exit()
		else:
			response = request.urlretrieve(sbdr_url, sbdr_name)

def downloadAdditionalDataTypes(cordar_file_name, segment_id, additional_data_type):
	# Download additional data types
	additional_data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/{1}".format(cordar_file_name, additional_data_type)
	logger.info("\n[TODO: does not currently download] '{0}': {1}".format(additional_data_type, additional_data_url))
	# TODO: add functionality for which files should be downloaded
	# This function does not currently have functionality in pydar

def extractFlybyDataImages(flyby_observation_num=None,
							flyby_id=None,
							segment_num=None,
							additional_data_types_to_download=[],
							resolution='I',
							top_x_resolutions=None):

	if flyby_id is not None and type(flyby_id) == str:
		flyby_id = flyby_id.upper() # ensure that observation number set to capitalized 'T'
	if flyby_observation_num is not None and type(flyby_observation_num) == str:
		while len(flyby_observation_num) < 4:
			flyby_observation_num = "0" + flyby_observation_num # set all radar take numbers to be four digits long: 229 -> 0229
	if top_x_resolutions is not None:
		resolution = None # set default resolution to None if selecting the top x resolutions

	# Error handling:
	pydar.errorHandlingExtractFlybyDataImages(flyby_observation_num=flyby_observation_num,
											flyby_id=flyby_id,
											segment_num=segment_num,
											additional_data_types_to_download=additional_data_types_to_download,
											resolution=resolution,
											top_x_resolutions=top_x_resolutions)

	logger.info("flyby_observation_num = {0}".format(flyby_observation_num))
	logger.info("flyby_id = {0}".format(flyby_id))
	logger.info("segment_num = {0}".format(segment_num))
	logger.info("additional_data_types_to_download = {0}".format(additional_data_types_to_download))
	logger.info("resolution = {0}".format(resolution))
	logger.info("top_x_resolutions = {0}".format(top_x_resolutions))

	download_files = True # for debugging, does not always download files before running data

	# update csv
	days_between_checking_jpl_website = 7 # set to 0 to re-run currently without waiting
	x_days_ago = datetime.now() - timedelta(days=days_between_checking_jpl_website)
	filetime = datetime.fromtimestamp(os.path.getctime(os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')))
	if filetime < x_days_ago:
		# File it more than X days old
		logger.info("file is older than {0} days, running html capture to update coradr_jpl_options.csv (will take about twenty minutes):".format(days_between_checking_jpl_website))
		pydar.csvCORADRJPLOptions() # coradr_jpl_options.csv
		pydar.csvSwathCoverage() # swath_coverage_by_time_position.csv
		pydar.csvFeatureNameDetails() #feature_name_details.csv

	if flyby_id is not None:  # convert flyby Id to an Observation Number
		flyby_observation_num = convertFlybyIDToObservationNumber(flyby_id)

	avaliable_flyby_id, avaliable_observation_numbers = getFlybyData()

	if flyby_observation_num not in avaliable_observation_numbers:
		logger.critical("Observation number '{0}' NOT FOUND in available observation numbers: {1}\n".format(flyby_observation_num, avaliable_observation_numbers))
		exit()
	else:
		logger.debug("Observation number '{0}' FOUND in available observation numbers: {1}\n".format(flyby_observation_num, avaliable_observation_numbers))

	# Download information from pds-imaging site for CORADR
	flyby_observation_cordar_name = retrieveJPLCoradrOptions(flyby_observation_num)
	if not os.path.exists('pydar_results'): os.makedirs('pydar_results')
	if not os.path.exists("pydar_results/{0}_{1}".format(flyby_observation_cordar_name, segment_num)): os.makedirs("pydar_results/{0}_{1}".format(flyby_observation_cordar_name, segment_num))

	if download_files:
		# AAREADME.TXT
		downloadAAREADME(flyby_observation_cordar_name, segment_num)
		
		# BIDR
		if top_x_resolutions is not None:
			downloadBIDRCORADRData(flyby_observation_cordar_name, segment_num, resolution_types[-top_x_resolutions:])
		else:
			downloadBIDRCORADRData(flyby_observation_cordar_name, segment_num, resolution)

		# SBDR
		downloadSBDRCORADRData(flyby_observation_cordar_name, segment_num)

		# Download additional data types
		for data_type in additional_data_types_to_download:
			if data_type not in ["BIDR", "SBDR"]: # ignore data files that have already been downloaded
				downloadAdditionalDataTypes(flyby_observation_cordar_name, segment_num, data_type)

	if len(os.listdir("pydar_results/{0}_{1}".format(flyby_observation_cordar_name, segment_num))) == 0:
		logger.critical("Unable to find any images with current parameters")
		exit()
