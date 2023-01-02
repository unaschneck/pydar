# Extract flyby parameters from CASSINI

import zipfile
import os

import pandas as pd
from planetaryimage import PDS3Image
import matplotlib.pyplot as plt
from urllib import request, error

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

if __name__ == '__main__':
	avaliable_flyby_id, avaliable_observation_numbers = getFlybyData()
	flyby_observiation_num = "0065"

	if flyby_observiation_num not in avaliable_observation_numbers:
		print("Observation number '{0}' NOT FOUND in avaiable observation numbers: {1}\n".format(flyby_observiation_num, avaliable_observation_numbers))
		exit()
	else:
		print("Observation number '{0}' FOUND in avaiable observation numbers: {1}\n".format(flyby_observiation_num, avaliable_observation_numbers))

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
		from bs4 import BeautifulSoup
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

	# Get information from pds-imaging site for image
	label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.LBL".format(more_accurate_model_number)
	label_name = label_url.split("/")[-1].split(".")[0] + ".txt"
	try:
		request.urlretrieve(label_url)
	except error.HTTPError as err:
		print("Unable to access: {0}\nError (and exiting): '{1}'".format(label_url, err.code))
		exit()
	else:
		response = request.urlretrieve(label_url, label_name)

	data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.ZIP".format(more_accurate_model_number)
	zipfile_name = data_url.split("/")[-1].split(".")[0] + ".zip"
	try:
		request.urlretrieve(data_url)
	except error.HTTPError as err:
		print("Unable to access: {0}\nError (and exiting): '{1}'".format(data_url, err.code))
		exit()
	else:
		response = request.urlretrieve(data_url, zipfile_name)
		with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
			zip_ref.extractall()

		print("Generating image...")
		from planetaryimage import PDS3Image
		zipped_image = zipfile_name.split(".")[0] + ".IMG"
		print("Zipped image: {0}".format(zipped_image))
		image = PDS3Image.open(zipped_image)
		fig = plt.figure(figsize=(8,8), dpi=120)
		plt.imshow(image.image, cmap='gray')
		plt.show()

		flyby_name = data_url.split("/")[-1].split(".")[0]
		os.remove("{0}.IMG".format(flyby_name))
		os.remove("{0}.txt".format(flyby_name))
		os.remove("{0}.zip".format(flyby_name))
