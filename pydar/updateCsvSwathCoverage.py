# Note: Script not accessible via __init__.py and is run directly by the developer and Github Actions
# updates swath_coverage_by_time_position.csv

# Built in Python functions
import logging
import os
import random

# External Python libraries (installed via pip install)
from bs4 import BeautifulSoup
import pandas as pd
from urllib import request, error

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

########################################################################

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

## FUNCTIONS TO WEB SCRAPE TO POPULATE swath_coverage_by_time_position.csv ################
def updateCsvSwathCoverage():
	# Update the csv script for swath_coverage_by_time_position.csv from the most recent JPL webpage
	# Retrieves information for each .LBL file that exists for CASSINI data files
	#		Estimated runtime: 15 minutes
	#		Returns: swath_coverage_by_time_position.csv in data/ folder

	logger.info("Refreshing: swath_coverage_by_time_position.csv")

	# Get all Titan Flybys with most up to date versions
	coradr_ids = []
	ids_with_no_bidr = []
	coradr_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'coradr_jpl_options.csv')  # get file's directory, up one level, /data/*.csv
	coradr_dataframe = pd.read_csv(coradr_csv_file)
	for index, row in coradr_dataframe.iterrows():
		row = row.tolist()
		if row[1] == True:
			if row[4] == False: # if is a Titan flyby but "Contains BIDR" is False
				ids_with_no_bidr.append(row[0])
			if coradr_ids != []:
				if coradr_ids[-1].split("_V")[0] in row[0]: # replace the older version with the most recent version
					coradr_ids[-1] = row[0]
				else:
					coradr_ids.append(row[0])
			else:
				coradr_ids.append(row[0])

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

	resolution_dict = {"B": 2, "D": 8, "F": 32, "G": 64, "H": 128, "I": 256} #  pixels/degree

	user_agents = [
		'Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
		'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
		'Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
	]
	random_agent = random.choice(user_agents)

	# Retrieve a list of all the .LBL for each CORADR ID (different for each resolution)
	lbl_information = []
	for radar_id in coradr_ids:
		if radar_id not in ids_with_no_bidr:
			base_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{radar_id}/DATA/BIDR/"
			req_with_headers = request.Request(url=base_url, headers={'User-Agent': random_agent})
			base_html = request.urlopen(req_with_headers).read()
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
						bidr_url = f"https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/{radar_id}/DATA/BIDR/{filename}"
						logger.info(f"Retrieving LBL information: {bidr_url}")
						lbl = [radar_id, None, None, None, None, None, None, None, None, None, None, None, None, None]
						lbl[1] = pydar.convertObservationNumberToFlybyID(radar_id.split("_")[1])
						lbl[2] = (filename.split("_")[2]).split("S")[1] # Segment Number
						lbl[3] = filename
						lbl[4] = filename[2] # Data Type
						lbl[5] = data_type_dict[filename[2]] # Data Type, with full title
						lbl[6] = resolution_dict[filename[4]] # Resolution
						with request.urlopen(bidr_url) as lbl_file:
							for line in (lbl_file.read().decode("UTF-8")).split("\n"):
								if "TARGET_NAME" in line:
									lbl[7] = line.split("=")[1].strip()
								if "MAXIMUM_LATITUDE" in line:
									max_lat = line.split("=")[1].strip()
									max_lat = max_lat.split("<")[0] 
									lbl[8] = max_lat
								if "MINIMUM_LATITUDE" in line:
									min_lat = line.split("=")[1].strip()
									min_lat = min_lat.split("<")[0] 
									lbl[9] = min_lat
								if "EASTERNMOST_LONGITUDE" in line:
									east_long = line.split("=")[1].strip()
									east_long = east_long.split("<")[0] 
									lbl[10] = east_long
								if "WESTERNMOST_LONGITUDE" in line:
									west_long = line.split("=")[1].strip()
									west_long = west_long.split("<")[0] 
									lbl[11] = west_long
								if "START_TIME" in line:
									lbl[12] = line.split("=")[1].strip()
								if "STOP_TIME" in line:
									lbl[13] = line.split("=")[1].strip()
							lbl_information.append(lbl)

	# Write to CSV
	header_options = ["CORADR ID",
					"FLYBY ID",
					"SEGMENT NUMBER",
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

if __name__ == '__main__':
	updateCsvSwathCoverage() # 		updates swath_coverage_by_time_position.csv
