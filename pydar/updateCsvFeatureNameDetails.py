# Note: Script not accessible via __init__.py and is run directly by the developer
# updates feature_name_details.csv

# Built in Python functions
import logging
import os
import re
import random

# External Python libraries (installed via pip install)
from bs4 import BeautifulSoup
import pandas as pd
from urllib import request, error

########################################################################

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

## FUNCTIONS TO WEB SCRAPE TO POPULATE feature_name_details.csv ################
def updateCsvFeatureNameDetails():
	# Update the csv script for feature_name_details.csv from the planetary names database
	# Retrieves information for each Titan feature
	#		Estimated runtime: 3 minutes
	#		Returns: feature_name_details.csv in data/ folder

	logger.info("Refreshing: feature_name_details.csv")

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

	# BeautifulSoup web scrapping to find Titan feature names with details
	logger.info("Retrieving observation information from https://planetarynames.wr.usgs.gov/SearchResults?Target=74_Titan....")
	titan_root_url = "https://planetarynames.wr.usgs.gov/SearchResults?Target=74_Titan"
	req_with_headers = request.Request(url=titan_root_url, headers={'User-Agent': random_agent})
	titan_html = request.urlopen(req_with_headers).read()
	soup = BeautifulSoup(titan_html, 'html.parser')
	ahref_feature_names = soup.findAll('a')
	ahref_lst = []
	for link in ahref_feature_names:
		feature_link = link.get('href')
		if feature_link is not None:
			if feature_link.startswith("/Feature/"):
				if feature_link != "/Feature/7014": # ignore a dropped column for 'Sotra Facula' (a feature that has been dropped from the table, but still exists)
					ahref_lst.append(feature_link)

	feature_options = []
	base_url = "https://planetarynames.wr.usgs.gov"
	for i, feature_ahref in enumerate(ahref_lst):
		feature_html = request.urlopen(base_url + feature_ahref)
		logger.info(f"[{i+1}/{len(ahref_lst)}] Retrieving: {base_url + feature_ahref}")
		soup = BeautifulSoup(feature_html, 'html.parser')
		tables = soup.find_all('table', class_='usa-table')
		# [Feature Name, Northmost Latitude, Southmost Latitude, Eastmost Longitude, Westmost Longitude, Center Latitude, Center Longitude, URL]
		feature_object = [None, None, None, None, None, None, None, None]
		for table in tables:
			for row in table.tbody.find_all("tr"):
				feature_row = ((row.text).lstrip()).split("\n")
				feature_row = [f.strip() for f in feature_row if f != '' and re.search(r'[a-zA-Z-?\d+]', f)]
				feature_object[7] = base_url + feature_ahref
				if len(feature_row) == 2:
					if feature_row[0] == "Feature Name":
						feature_object[0] = feature_row[1]
					if feature_row[0] == "Northmost Latitude":
						feature_object[1] = feature_row[1].split(" ")[0]
					if feature_row[0] == "Southmost Latitude":
						feature_object[2] = feature_row[1].split(" ")[0]
					if feature_row[0] == "Eastmost Longitude":
						feature_object[3] = feature_row[1].split(" ")[0]
					if feature_row[0] == "Westmost Longitude":
						feature_object[4] = feature_row[1].split(" ")[0]
					if feature_row[0] == "Center Latitude":
						feature_object[5] = feature_row[1].split(" ")[0]
					if feature_row[0] == "Center Longitude":
						feature_object[6] = feature_row[1].split(" ")[0]
		feature_options.append(feature_object)

	# Add Huygens landing site manually
	huygens_landing_site = ["Huygens Landing Site", 
							"-10.576",
							"-10.576",
							"167.547",
							"167.547",
							"-10.576",
							"167.547",
							"https://pds-imaging.jpl.nasa.gov/documentation/Cassini_RADAR_Users_Guide_2nd_Ed_191004_cmp_200421.pdf#page=165"]
	feature_options.append(huygens_landing_site)

	# Write to CSV
	header_options = ["Feature Name", 
					"Northmost Latitude",
					"Southmost Latitude",
					"Eastmost Longitude",
					"Westmost Longitude",
					"Center Latitude",
					"Center Longitude", 
					"URL"]
	df = pd.DataFrame(feature_options, columns=header_options)
	df = df.sort_values(by=["Feature Name"])
	df.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'feature_name_details.csv'), header=header_options, index=False)

if __name__ == '__main__':
	updateCsvFeatureNameDetails() #	updates feature_name_details.csv
