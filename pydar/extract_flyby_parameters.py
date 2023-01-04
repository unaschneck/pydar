# Extract flyby parameters from CASSINI

import zipfile
import os
import csv 
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

def getFlybyData():
	# Header: Titan flyby id, Radar Data Take Number, Sequence number, Orbit Number/ID
	flyby_id = []
	flby_radar_take_num = []
	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		row = row.tolist()
		flyby_id.append(row[0])
		radar_take_num = row[1].split(" ")[1]
		while len(radar_take_num) < 4:
			radar_take_num = "0" + radar_take_num # set all radar take numbers to be four digits long: 229 -> 0229
		flby_radar_take_num.append(radar_take_num)
	# returns a list of flyby IDs and associated Radar Data Take Number
	return flyby_id, flby_radar_take_num

def convertFlybyIDToObservationNumber(flyby_id):
	# convert Flyby ID to Observation Number to find data files
	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/*.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		if row[0] == flyby_id: # TODO; Add error handling to include only valiid flyby IDs
			observation_number = row[1].split(" ")[1]
			while len(observation_number) < 4:
				observation_number = "0" + observation_number # set all radar take numbers to be four digits long: 229 -> 0229
	return observation_number

def retrieveJPLCoradrOptions(flyby_observiation_num):
	# runs to access the most up to date optiosn from the JPL webpage
	days_between_checking_jpl_website = 2 # set to 0 to re-run currently without waiting
	x_days_ago = datetime.now() - timedelta(days=days_between_checking_jpl_website)
	
	filetime = datetime.fromtimestamp(os.path.getctime(os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')))
	if filetime < x_days_ago:
		# File it more than X days old
		logger.info("file is older than {0} days, running html capture for CORADR options:".format(days_between_checking_jpl_website))
	
		# BeautifulSoup web scrapping to find observation file number full title
		logger.info("Retrieving observation information from pds-imaging.jpl.nasa.gov/ata/cassini/cassini_orbital....")
		cassini_root_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter"
		cassini_html = request.urlopen(cassini_root_url).read()
		soup = BeautifulSoup(cassini_html, 'html.parser')
		table = soup.find('table', {"id": "indexlist"})
		table_text = (table.text).split("\n")
		coradr_options = []
		for txt in table_text:
			if 'CORADR' in txt:
				coradr_title = txt.split('/')[0]
				if '.' not in coradr_title:
					coradr_options.append(coradr_title)
		# Wrte to CSV
		header_options = ["CORADR ID Options"]
		df = pd.DataFrame(coradr_options, columns=header_options)
		df = df.sort_values(by=["CORADR ID Options"])
		df.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv'), header=header_options, index=False)

	# Read from CSV
	jpl_coradr_options = []
	coradr_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
	coradr_dataframe = pd.read_csv(coradr_csv_file)
	for index, row in coradr_dataframe.iterrows():
		row = row.tolist()
		jpl_coradr_options.append(row[0])

	find_cordar_listing = 'CORADR_{0}'.format(flyby_observiation_num)
	version_types_avaliable = list(filter(lambda x: find_cordar_listing in x, jpl_coradr_options))
	more_accurate_model_number = version_types_avaliable[-1] # always choose the last and more up to date version number
	logger.info("Most recent version avaliable = {0} from available {1}".format(more_accurate_model_number, version_types_avaliable))
	return more_accurate_model_number

def downloadCORADRData(cordar_file_name, segment_id, resolution_px):
	base_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/".format(cordar_file_name)
	logger.info("Retrieving filenames from: {0}\n".format(base_url))

	# Retrieve a list of all elements from the base URL to download
	base_html = request.urlopen(base_url).read()
	soup = BeautifulSoup(base_html, 'html.parser')
	table = soup.find('table', {"id": "indexlist"})
	table_text = (table.text).split("\n")
	url_filenames = []
	all_bi_files = []
	for txt in table_text:
		if txt.startswith('BI'):
			filename = (txt.split('/')[0]).split(".")[0]
			if 'LBL' in (txt.split('/')[0]).split(".")[1]:
				filename += '.LBL'
			if 'ZIP' in (txt.split('/')[0]).split(".")[1]:
				filename += '.ZIP'
			all_bi_files.append(filename)
			if segment_id in filename: # only save certain segements
				for resolution in resolution_px: # only save top x resolutions
					if "BIBQ{0}".format(resolution) in filename:
						url_filenames.append(filename)

	logger.info("All files found with specified resolution, segment, and flyby identification: {0}\n".format(url_filenames))
	if len(url_filenames) == 0:
		logger.critical("No files found with resolution, segment, and flyby identification. Please use different parameters to retrieve data.\nAll BI files found: {0}".format(all_bi_files))
		exit()

	for i, coradr_file in enumerate(url_filenames):
		if 'LBL' in coradr_file:
			label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(cordar_file_name, coradr_file)
			logger.info("Retrieving [{0}/{1}]: {2}".format(i+1, len(url_filenames), label_url))
			label_name = label_url.split("/")[-1].split(".")[0] + ".txt"
			label_name = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id), label_name)
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
			zipfile_name = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id), zipfile_name)
			try:
				request.urlretrieve(data_url)
			except error.HTTPError as err:
				logger.info("Unable to access: {0}\nError (and exiting): '{1}'".format(data_url, err.code))
				exit()
			else:
				response = request.urlretrieve(data_url, zipfile_name)
				zipped_image = zipfile_name.split(".")[0] + ".IMG"
				with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
					zipped_image_path = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id))
					zip_ref.extractall(zipped_image_path)

def extractFlybyDataImages(flyby_observation_num=None,
							flyby_id=None,
							segment_num=None,
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
	pydar.errorHandling(flyby_observation_num=flyby_observation_num,
						flyby_id=flyby_id,
						segment_num=segment_num,
						resolution=resolution,
						top_x_resolutions=top_x_resolutions)

	logger.info("flyby_observation_num = {0}".format(flyby_observation_num))
	logger.info("flyby_id = {0}".format(flyby_id))
	logger.info("segment_num = {0}".format(segment_num))
	logger.info("resolution = {0}".format(resolution))
	logger.info("top_x_resolutions = {0}".format(top_x_resolutions))

	download_files = True # for debugging, does not always download files before running data

	if flyby_id is not None:  # convert flyby Id to an Observation Number
		flyby_observation_num = convertFlybyIDToObservationNumber(flyby_id)

	avaliable_flyby_id, avaliable_observation_numbers = getFlybyData()

	if flyby_observation_num not in avaliable_observation_numbers:
		logger.critical("Observation number '{0}' NOT FOUND in available observation numbers: {1}\n".format(flyby_observation_num, avaliable_observation_numbers))
		exit()
	else:
		logger.debug("Observation number '{0}' FOUND in available observation numbers: {1}\n".format(flyby_observation_num, avaliable_observation_numbers))

	# Download information from pds-imaging site for image
	flyby_observation_cordar_name = retrieveJPLCoradrOptions(flyby_observation_num)
	if not os.path.exists('results'): os.makedirs('results')
	if not os.path.exists("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num)): os.makedirs("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num))

	if download_files: 
		if top_x_resolutions is not None:
			downloadCORADRData(flyby_observation_cordar_name, segment_num, resolution_types[-top_x_resolutions:])
		else:
			downloadCORADRData(flyby_observation_cordar_name, segment_num, resolution)
	if len(os.listdir("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num))) == 0:
		logger.critical("Unable to find any images with current parameters")
		exit()
