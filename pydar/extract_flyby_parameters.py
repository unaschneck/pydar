# Extract flyby parameters from CASSINI

# Built in Python functions
from datetime import datetime, timedelta
import os
import zipfile

# External Python libraries (installed via pip install)
from bs4 import BeautifulSoup
import logging
import pandas as pd
from urllib import request, error

# Internal Pydar reference to access functions, global variables, and error handling
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
		if row.iloc[0] == flyby_id:
			observation_number = row.iloc[1].split(" ")[1]
			while len(observation_number) < 4:
				observation_number = "0" + observation_number # set all radar take numbers to be four digits long: 229 -> 0229
			return observation_number

def convertObservationNumberToFlybyID(flyby_observation_num=None):
	# convert Flyby ID to Observation Number to find data files
	if flyby_observation_num is not None:
		if type(flyby_observation_num) != str:
			raise ValueError(f"[flyby_observation_num]: Must be a str, current type = '{type(flyby_observation_num)}'")
		else:
			while len(flyby_observation_num) < 4:
				flyby_observation_num = "0" + flyby_observation_num # set all radar take numbers to be four digits long: 229 -> 0229

	pydar.errorHandlingConvertObservationNumberToFlybyID(flyby_observation_num=flyby_observation_num)

	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		take_ob_num = "0" + row.iloc[1].split(" ")[1]
		if take_ob_num == flyby_observation_num:
			return row.iloc[0] # returns flyby ID

def retrieveJPLCoradrOptions():
	# Read JPL Options from CSV
	coradr_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
	coradr_dataframe = pd.read_csv(coradr_csv_file)
	return coradr_dataframe

def retrieveMostRecentVersionNumber(flyby_observiation_num=None):
	# Return the CORADAR value with the most recent version from a list of possible options
	coradr_dataframe = retrieveJPLCoradrOptions()
	jpl_coradr_options = []
	for index, row in coradr_dataframe.iterrows():
		row = row.tolist()
		jpl_coradr_options.append(row[0])

	find_cordar_listing = f"CORADR_{flyby_observiation_num}"
	version_types_available = list(filter(lambda x: find_cordar_listing in x, jpl_coradr_options))
	more_accurate_model_number = version_types_available[-1] # always choose the last and more up to date version number (Currently, v3)
	logger.info(f"Most recent CORADR version is {more_accurate_model_number} from the available list {version_types_available}")
	return more_accurate_model_number

def retrieveCoradrWithoutBIDR():
	# Return a list of valid flyby observation numbers that do not contain BIDR
	coradr_dataframe = retrieveJPLCoradrOptions()
	coradar_without_bidr = []
	for index, row in coradr_dataframe.iterrows():
		if row["Is a Titan Flyby"]: # check only flybys that are valid Titan flybys
			if "V" not in row["CORADR ID"] and row["Contains BIDR"] is False: # if not a version row, and does not contain BIDR
				coradar_without_bidr.append(row["CORADR ID"].split("_")[1]) # store the observation number from the CORADR
	return coradar_without_bidr

def downloadAAREADME(cordar_file_name, segment_id):
	# Download AAREADME.txt within a CORADR directory
	aareadme_name = "AAREADME.TXT"
	aareadme_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/{aareadme_name}"

	# Retrieve a list of all elements from the base URL to download AAREADME.txt
	logger.info(f"Retrieving {cordar_file_name} {aareadme_name}")
	aareadme_name = os.path.join(f"pydar_results/{cordar_file_name}_{segment_id}", aareadme_name)
	try:
		request.urlretrieve(aareadme_url)
	except error.HTTPError as err:
		raise HTTPError(f"Unable to access: {aareadme_url}\nError (and exiting): '{err.code}'")
	else:
		response = request.urlretrieve(aareadme_url, aareadme_name)

def downloadBIDRCORADRData(cordar_file_name, segment_id, resolution_px):
	# Download BDIR files
	base_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/BIDR/"
	logger.info(f"Retrieving BIDR filenames from: {base_url}\n")

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
			if segment_id in filename: # only save certain segments
				for resolution in resolution_px: # only save top x resolutions
					bi_types = ["B", "E", "T", "N", "M", "L"] # BI<OPTION>Q<RESOLUTION>
					for bi in bi_types:
						if f"BI{bi}Q{resolution}" in filename:
							url_filenames.append(filename)

	logger.info(f"All BIDR files found with specified resolution, segment, and flyby identification: {url_filenames}\n")
	if len(url_filenames) == 0:
		raise ValueError(f"No BIDR files found with resolution, segment, and flyby identification. Please use different parameters to retrieve data.\nAll files found: {all_bidr_files}")

	for i, coradr_file in enumerate(url_filenames):
		if 'LBL' in coradr_file:
			label_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/BIDR/{coradr_file}"
			logger.info(f"Retrieving [{i+1}/{len(url_filenames)}]: {label_url}")
			label_name = label_url.split("/")[-1].split(".")[0] + ".LBL"
			label_name = os.path.join(f"pydar_results/{cordar_file_name}_{segment_id}", label_name)
			try:
				request.urlretrieve(label_url)
			except error.HTTPError as err:
				raise HTTPError(f"Unable to access: {label_url}\nError (and exiting): '{err.code}'")
			else:
				response = request.urlretrieve(label_url, label_name)
		if 'ZIP' in coradr_file:
			data_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/BIDR/{coradr_file}"
			logger.info(f"Retrieving [{i+1}/{len(url_filenames)}]: {data_url}")
			zipfile_name = data_url.split("/")[-1].split(".")[0] + ".zip"
			zipfile_name = os.path.join(f"pydar_results/{cordar_file_name}_{segment_id}", zipfile_name)
			try:
				request.urlretrieve(data_url)
			except error.HTTPError as err:
				raise HTTPError(f"Unable to access: {data_url}\nError (and exiting): '{err.code}'")
			else:
				response = request.urlretrieve(data_url, zipfile_name)
				zipped_image = zipfile_name.split(".")[0] + ".IMG"
				with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
					zipped_image_path = os.path.join(f"pydar_results/{cordar_file_name}_{segment_id}")
					zip_ref.extractall(zipped_image_path)

def downloadSBDRCORADRData(cordar_file_name, segment_id):
	# Download SBDR files
	base_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/SBDR/"
	logger.info(f"\nRetrieving SBDR filenames from: {base_url}")

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
		raise ValueError("No SBDR files were found with resolution, segment, and flyby identification. Please use different parameters to retrieve data")

	for sbdr_file in sbdr_files:
		sbdr_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/SBDR/{sbdr_file}"
		logger.info(f"Retrieving SBDR file '{sbdr_file}': {sbdr_url}")
		sbdr_name = os.path.join(f"pydar_results/{cordar_file_name}_{segment_id}", sbdr_file)
		try:
			request.urlretrieve(sbdr_url)
		except error.HTTPError as err:
			raise HTTPError(f"Unable to access: {sbdr_url}\nError (and exiting): '{err.code}'")
		else:
			response = request.urlretrieve(sbdr_url, sbdr_name)

def downloadAdditionalDataTypes(cordar_file_name, segment_id, additional_data_type):
	# Download additional data types
	additional_data_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{cordar_file_name}/DATA/{additional_data_type}"
	logger.info(f"\n[TODO: does not currently download] '{additional_data_type}': {additional_data_url}")
	# TODO: add functionality for which files should be downloaded
	# This function does not currently have functionality in pydar

def extractFlybyDataImages(flyby_observation_num=None,
							flyby_id=None,
							segment_num=None,
							additional_data_types_to_download=[],
							resolution='I',
							top_x_resolutions=None):

	if flyby_id is not None and type(flyby_id) == str:
		flyby_id = flyby_id.capitalize() # ensure that observation number set to capitalized 'T'
	if flyby_observation_num is not None and type(flyby_observation_num) == str:
		while len(flyby_observation_num) < 4:
			flyby_observation_num = "0" + flyby_observation_num # set all radar take numbers to be four digits long: 229 -> 0229
	if top_x_resolutions is not None:
		#logger.info("\nINFO: [top_x_resolutions] in use, overriding resolution '{0}' to save the top {1} resolutions".format(resolution, top_x_resolutions))
		resolution = None # set default resolution to None if selecting the top x resolutions

	# Error handling:
	pydar.errorHandlingExtractFlybyDataImages(flyby_observation_num=flyby_observation_num,
											flyby_id=flyby_id,
											segment_num=segment_num,
											additional_data_types_to_download=additional_data_types_to_download,
											resolution=resolution,
											top_x_resolutions=top_x_resolutions)

	logger.debug(f"flyby_observation_num = {flyby_observation_num}")
	logger.debug(f"flyby_id = {flyby_id}")
	logger.debug(f"segment_num = {segment_num}")
	logger.debug(f"additional_data_types_to_download = {additional_data_types_to_download}")
	logger.debug(f"resolution = {resolution}")
	logger.debug(f"top_x_resolutions = {top_x_resolutions}")

	download_files = True # for debugging, does not always download files before running data

	if flyby_id is not None:  # convert flyby Id to an Observation Number
		flyby_observation_num = convertFlybyIDToObservationNumber(flyby_id)

	# Data gaps and problems from the original downlinking and satellite location, report some special cases to user
	no_associated_bidr_values = retrieveCoradrWithoutBIDR() # currently: ["0048", "0186", "0189", "0209", "0234"]
	if flyby_observation_num in no_associated_bidr_values:
		logger.info("\nINFO: due to data gaps or issues with downlinking, flyby does not have not have associated BIDR data.")
		if flyby_observation_num == "0048":
			logger.info("0048 (T4) did not have SAR data, only scatterometry and radiometry\n")
		elif flyby_observation_num == "0186":
			logger.info("0186 (T52) only has radiometery and compressed scatterometry\n")
		elif flyby_observation_num == "0189":
			logger.info("0189 (T53) only has radiometery and compressed scatterometry\n")
		elif flyby_observation_num == "0209":
			logger.info("0209 (T63) only has scatterometry and radiometry\n")
		elif flyby_observation_num == "0234":
			logger.info("0234 (T80) only has scatterometry and radiometry\n")
		else:
			logger.info(f"{flyby_observation_num} does not BIDR data\n") # possible catch for new files found without BIDR

	available_flyby_id, available_observation_numbers = getFlybyData()

	if flyby_observation_num not in available_observation_numbers:
		raise ValueError(f"Observation number '{flyby_observation_num}' NOT FOUND in available observation numbers: {available_observation_numbers}\n")
	else:
		logger.debug(f"Observation number '{flyby_observation_num}' FOUND in available observation numbers: {available_observation_numbers}\n")

	# Download information from pds-imaging site for CORADR
	flyby_observation_cordar_name = retrieveMostRecentVersionNumber(flyby_observation_num)
	if not os.path.exists('pydar_results'): os.makedirs('pydar_results')
	if not os.path.exists(f"pydar_results/{flyby_observation_cordar_name}_{segment_num}"): 
		os.makedirs(f"pydar_results/{flyby_observation_cordar_name}_{segment_num}")

	if download_files:
		# Download AAREADME.TXT
		downloadAAREADME(flyby_observation_cordar_name, segment_num)
		
		# Download BIDR
		if flyby_observation_num not in no_associated_bidr_values: # only attempt to download BIDR files for flybys that have BIDR files
			if top_x_resolutions is not None:
				downloadBIDRCORADRData(flyby_observation_cordar_name, segment_num, resolution_types[-top_x_resolutions:])
			else:
				downloadBIDRCORADRData(flyby_observation_cordar_name, segment_num, resolution)

		# Download SBDR
		downloadSBDRCORADRData(flyby_observation_cordar_name, segment_num)

		# Download additional data types (TODO)
		for data_type in additional_data_types_to_download:
			if data_type not in ["BIDR", "SBDR"]: # ignore data files that have already been downloaded
				downloadAdditionalDataTypes(flyby_observation_cordar_name, segment_num, data_type)

	# No valid parameters given, empty file
	if len(os.listdir(f"pydar_results/{flyby_observation_cordar_name}_{segment_num}")) == 0:
		logger.critical(f"\npydar_results/{flyby_observation_cordar_name}_{segment_num} is empty. Unable to find any data files with current parameters")
