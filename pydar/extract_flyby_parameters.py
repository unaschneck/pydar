# Extract flyby parameters from CASSINI

import zipfile
import os

import pandas as pd
from planetaryimage import PDS3Image
import matplotlib.pyplot as plt
from urllib import request, error

from bs4 import BeautifulSoup


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

def retrieveJPLCoradrOptions(flyby_observiation_num):
	# runs to access the most up to date optiosn from the JPL webpage
	import csv 
	from datetime import datetime, timedelta
	days_between_checking_jpl_website = 2 # set to 0 to re-run currently without waiting
	x_days_ago = datetime.now() - timedelta(days=days_between_checking_jpl_website)
	
	filetime = datetime.fromtimestamp(os.path.getctime(os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')))
	if filetime < x_days_ago:
		# File it more than X days old
		print("file is older than {0} days, running html capture for CORADR options:".format(days_between_checking_jpl_website))
	
		# BeautifulSoup web scrapping to find observation file number full title
		print("Retrieving observation information from pds-imaging.jpl.nasa.gov/ata/cassini/cassini_orbital....")
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
		print(coradr_options)
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
	# Version 1: Archived early when Titan obliquity is assumed to be zero
	# Version 2: Early attempt to fix problem using Titan spin model
	# Version 3: Long term accurate spin model and additional accuracy improvements
	more_accurate_model_number = version_types_avaliable[-1] # always choose the last and more up to date version number
	print("Most recent version avaliable = {0} from avalible {1}".format(more_accurate_model_number, version_types_avaliable))
	return more_accurate_model_number

def downloadCORADRData(cordar_file_name, segment_id, resolution_px):
	base_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/".format(cordar_file_name)
	print("Retrieving filenames from: {0}".format(base_url))

	# Retrieve a list of all elements from the base URL to download
	base_html = request.urlopen(base_url).read()
	soup = BeautifulSoup(base_html, 'html.parser')
	table = soup.find('table', {"id": "indexlist"})
	table_text = (table.text).split("\n")
	url_filenames = []
	for txt in table_text:
		if txt.startswith('BI'):
			filename = (txt.split('/')[0]).split(".")[0]
			if 'LBL' in (txt.split('/')[0]).split(".")[1]:
				filename += '.LBL'
			if 'ZIP' in (txt.split('/')[0]).split(".")[1]:
				filename += '.ZIP'
			if segment_id in filename: # only save certain segements
				for resolution in resolution_px: # only save top x resolutions
					if "BIBQ{0}".format(resolution) in filename:
						url_filenames.append(filename)
	print(url_filenames)

	for i, coradr_file in enumerate(url_filenames):
		if 'LBL' in coradr_file:
			label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(cordar_file_name, coradr_file)
			print("Retrieving [{0}/{1}]: {2}".format(i, len(url_filenames), label_url))
			label_name = label_url.split("/")[-1].split(".")[0] + ".txt"
			label_name = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id), label_name)
			try:
				request.urlretrieve(label_url)
			except error.HTTPError as err:
				print("Unable to access: {0}\nError (and exiting): '{1}'".format(label_url, err.code))
				exit()
			else:
				response = request.urlretrieve(label_url, label_name)
		if 'ZIP' in coradr_file:
			data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(cordar_file_name, coradr_file)
			print("Retrieving [{0}/{1}]: {2}".format(i, len(url_filenames), data_url))
			zipfile_name = data_url.split("/")[-1].split(".")[0] + ".zip"
			zipfile_name = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id), zipfile_name)
			try:
				request.urlretrieve(data_url)
			except error.HTTPError as err:
				print("Unable to access: {0}\nError (and exiting): '{1}'".format(data_url, err.code))
				exit()
			else:
				response = request.urlretrieve(data_url, zipfile_name)
				zipped_image = zipfile_name.split(".")[0] + ".IMG"
				with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
					zipped_image_path = os.path.join("results/{0}_{1}".format(cordar_file_name, segment_id))
					zip_ref.extractall(zipped_image_path)

def extractFlybyDataImages(flyby_observiation_num=None,
							segment_num=None,
							top_x_resolutions=None):

	avaliable_flyby_id, avaliable_observation_numbers = getFlybyData()
	download_files = True

	resolution_types = ["B", "D", "F", "H", "I"] # 2, 8, 32, 128, 256 pixels/degree

	if flyby_observiation_num not in avaliable_observation_numbers:
		print("Observation number '{0}' NOT FOUND in avaiable observation numbers: {1}\n".format(flyby_observiation_num, avaliable_observation_numbers))
		exit()
	else:
		print("Observation number '{0}' FOUND in avaiable observation numbers: {1}\n".format(flyby_observiation_num, avaliable_observation_numbers))

	flyby_observation_cordar_name = retrieveJPLCoradrOptions(flyby_observiation_num)
	# Download information from pds-imaging site for image
	if not os.path.exists('results'): os.makedirs('results')
	if not os.path.exists("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num)): os.makedirs("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num))
	if download_files: 
		downloadCORADRData(flyby_observation_cordar_name, segment_num, resolution_types[-top_x_resolutions:])

	for filename in os.listdir("results/{0}_{1}".format(flyby_observation_cordar_name, segment_num)):
		if 'IMG' in filename:
			print("Generating image...")
			image_file = os.path.join("results/{0}_{1}/{2}".format(flyby_observation_cordar_name, segment_num, filename))
			from planetaryimage import PDS3Image
			print("Image: {0}".format(image_file))
			image = PDS3Image.open(image_file)
			fig = plt.figure(figsize=(4,6), dpi=120)
			plt.title(filename)
			plt.xlabel("Pixels #")
			plt.ylabel("Pixels #")
			plt.imshow(image.image, cmap='gray')
	plt.show()
