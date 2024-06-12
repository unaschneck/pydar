# Note: Script not accessible via __init__.py and is run directly by the developer
# updates coradr_jpl_options.csv

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

## FUNCTIONS TO WEB SCRAPE TO POPULATE coradr_jpl_options.csv ################
def updateCsvCORADRJPLOptions():
	# Update the csv script for coradr_jpl_options.csv from the most recent JPL webpage
	# Retrieves information for each CORADAR option and the data types it has available
	#		Estimated runtime: 5 minutes
	#		Returns: coradr_jpl_options.csv in data/ folder

	logger.info("Refreshing: coradr_jpl_options.csv")

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

	# BeautifulSoup web scrapping to find CASSINI data types
	logger.info("Retrieving observation information from planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbital....")
	cassini_root_url = "https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter"
	req_with_headers = request.Request(url=cassini_root_url, headers={'User-Agent': random_agent})
	cassini_html = request.urlopen(req_with_headers).read()
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
		coradr_url = f"{cassini_root_url}/{coradr_id[0]}/DATA"
		logger.info(f"Retrieving data types [{i+1}/{len(coradr_options)}]: {coradr_url}")
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

	# Write to CSV
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

if __name__ == '__main__':
	updateCsvCORADRJPLOptions() # 	updates coradr_jpl_options.csv
