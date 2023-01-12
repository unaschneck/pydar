# Update CSVs

import logging
import os

from bs4 import BeautifulSoup
import pandas as pd
from urllib import request, error

import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def csvCORADRJPLOptions():
	# runs to access the most up to date optiosn from the JPL webpage
	# Generate: coradr_jpl_options.csv

	# BeautifulSoup web scrapping to find observation file number full title
	logger.info("Refreshing: coradr_jpl_options.csv")
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
				coradr_options.append([coradr_title, False, False, False, False, False, False, False])
		_, flyby_radar_take_num = pydar.getFlybyData()

	# Check of CORADR has specific data files formats
	for i, coradr_id in enumerate(coradr_options):
		coradr_url = "{0}/{1}/DATA".format(cassini_root_url, coradr_id[0])
		logger.info("Retrieving data types [{0}/{1}]: {2}".format(i+1, len(coradr_options), coradr_url))
		coradr_html = request.urlopen(coradr_url).read()
		soup = BeautifulSoup(coradr_html, 'html.parser')
		table = soup.find('table', {"id": "indexlist"})
		table_text = (table.text).split("\n")
		for txt in table_text:
			for i, data_type in enumerate(pydar.datafile_types_columns):
				if data_type in txt:
					coradr_id[i+2] = True
				if coradr_id[0].split("_")[1] in flyby_radar_take_num:
					coradr_id[1] = True # Is a Titan Flyby

	# Wrte to CSV
	header_options = ["CORADR ID",
					"Is a Titan Flyby",
					"Contains ABDR",
					"Contains ASUM",
					"Contains BIDR",
					"Contains LBDR",
					"Contains SBDR",
					"Contains STDR"]
	df = pd.DataFrame(coradr_options, columns=header_options)
	df = df.sort_values(by=["CORADR ID"])
	df.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv'), header=header_options, index=False)

def csvSwathCoverage():
	# generate swath_coverage_by_time_position.csv
	# Estimated runtime: 15 minutes
	logger.info("Refreshing: swath_coverage_by_time_position.csv")

	# Get all Titan Flybys with most up to date versions
	coradr_ids = []
	coradr_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
	coradr_dataframe = pd.read_csv(coradr_csv_file)
	for index, row in coradr_dataframe.iterrows():
		row = row.tolist()
		if row[1] == True:
			if coradr_ids != []:
				if coradr_ids[-1].split("_V")[0] in row[0]: # replace the older version with the most recent version
					coradr_ids[-1] = row[0]
				else:
					coradr_ids.append(row[0])
			else:
				coradr_ids.append(row[0])

	# Retrieve a list of all the .lbl for each CORADR ID (different for each resolution)
	data_type_dict = {"F":"Primary Dataset (Linear Scale)", 
					"B": "Primary Dataset in Unsigned Byte Format (Normalized dB)",
					"S": "Normalized SAR (Physical Scale) with Thermal/Quantized Noise Removed",
					"X": "Noise for SAR without Incidence Angle Correction (Physical Scale)",
					"U":"Sigma0 without Incidence Angle (Linear Scale)", 
					"D": "Subtracted STD SAR",
					"E":"Incidence Angle Map", 
					"T":"Latitude Map",
					"N":"Longitude Map",
					"M":"Beam Mask Map",
					"L":"Number of Looks Map"}
	resolution_dict = {"B":2, "D":8, "F":32, "G": 64, "H":128, "I":256} #  pixels/degree
	lbl_information = []
	no_bidr = ["CORADR_0048", "CORADR_0186", "CORADR_0189", "CORADR_0209", "CORADR_0234"] # TODO: collect dynamically, check if has a BIDR when saving
	for radar_id in coradr_ids:
		if radar_id not in no_bidr:
			base_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/".format(radar_id)
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
						lbl = []
						filename += '.LBL'
						bidr_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/{0}/DATA/BIDR/{1}".format(radar_id, filename)
						logger.info("Retrieving LBL information: {0}".format(bidr_url))
						lbl = [radar_id, None, None, None, None, None, None, None, None, None, None, None, None]
						lbl[1] = pydar.convertObservationNumberToFlybyID(radar_id.split("_")[1])
						lbl[2] = filename
						lbl[3] = filename[2] # Data Type
						lbl[4] = data_type_dict[filename[2]] # Data Type
						lbl[5] = resolution_dict[filename[4]] # Resolution
						with request.urlopen(bidr_url) as lbl_file:
							for line in (lbl_file.read().decode("UTF-8")).split("\n"):
								if "TARGET_NAME" in line:
									lbl[6] = line.split("=")[1].strip()
								if "MAXIMUM_LATITUDE" in line:
									max_lat = line.split("=")[1].strip()
									max_lat = max_lat.split("<")[0] 
									lbl[7] = max_lat
								if "MINIMUM_LATITUDE" in line:
									min_lat = line.split("=")[1].strip()
									min_lat = min_lat.split("<")[0] 
									lbl[8] = min_lat
								if "EASTERNMOST_LONGITUDE" in line:
									east_long = line.split("=")[1].strip()
									east_long = east_long.split("<")[0] 
									lbl[9] = east_long
								if "WESTERNMOST_LONGITUDE" in line:
									west_long = line.split("=")[1].strip()
									west_long = west_long.split("<")[0] 
									lbl[10] = west_long
								if "START_TIME" in line:
									lbl[11] = line.split("=")[1].strip()
								if "STOP_TIME" in line:
									lbl[12] = line.split("=")[1].strip()
							lbl_information.append(lbl)

	# Wrte to CSV
	header_options = ["CORADR ID",
					"FLYBY ID",
					"FILENAME",
					"DATE TYPE SYMBOL",
					"DATE TYPE",
					"RESOLUTION (pixels/degrees)",
					"TARGET_NAME",
					"MAXIMUM_LATITUDE (Degrees)",
					"MINIMUM_LATITUDE (Degrees)",
					"EASTERNMOST_LONGITUDE (Degrees)",
					"WESTERNMOST_LONGITUDE (Degrees)",
					"START_TIME",
					"STOP_TIME"
					]
	df = pd.DataFrame(lbl_information, columns=header_options)
	df = df.sort_values(by=["CORADR ID"])
	df.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'swath_coverage_by_time_position.csv'), header=header_options, index=False)