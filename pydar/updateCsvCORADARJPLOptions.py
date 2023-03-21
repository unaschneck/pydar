# Note: Script not accessible via __init__.py and is run directly by the developer
# updates coradr_jpl_options.csv

# Built in Python functions
import logging
import os

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

	# BeautifulSoup web scrapping to find CASSINI data types
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

if __name__ == '__main__':
	updateCsvCORADRJPLOptions() # 	updates coradr_jpl_options.csv
