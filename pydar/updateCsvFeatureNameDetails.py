# Note: Script not accessible via __init__.py and is run directly by the developer
# updates feature_name_details.csv

# Built in Python functions
import logging
import os
import re

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

	# BeautifulSoup web scrapping to find Titan feature names with details
	logger.info("Retrieving observation information from https://planetarynames.wr.usgs.gov/SearchResults?Target=74_Titan....")
	titan_root_url = "https://planetarynames.wr.usgs.gov/SearchResults?Target=74_Titan"
	titan_html = request.urlopen(titan_root_url).read()
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
		logger.info("[{0}/{1}] Retrieving: {2}".format(i+1, len(ahref_lst), base_url + feature_ahref))
		soup = BeautifulSoup(feature_html, 'html.parser')
		table = soup.find("div", {"id":"layout_content_wrapper"})
		tr = table.find_all("tr")
		feature_object = [None, None, None, None, None, None, None, None]
		for i in tr:
			feature_row = ((i.text).lstrip()).split("\n")
			feature_row = [f.strip() for f in feature_row if f != '' and re.search('[a-zA-Z-?\d+]', f)]
			if len(feature_row) == 2:
				if feature_row[0] == "Feature Name":
					feature_object[0] = feature_row[1]
				if feature_row[0] == "Northernmost Latitude":
					feature_object[1] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Southernmost Latitude":
					feature_object[2] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Easternmost Longitude":
					feature_object[3] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Westernmost Longitude":
					feature_object[4] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Center Latitude":
					feature_object[5] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Center Longitude":
					feature_object[6] = feature_row[1].split(" ")[0]
				if feature_row[0] == "Origin":
					feature_object[7] = feature_row[1]
		feature_options.append(feature_object)

	# Add Huygens landing site manually
	huygens_landing_site = ["Huygens Landing Site", 
							"-10.576",
							"-10.576",
							"167.547",
							"167.547",
							"-10.576",
							"167.547",
							"where the Huygens probe landed east Adiri"]
	feature_options.append(huygens_landing_site)

	# Wrte to CSV
	header_options = ["Feature Name", 
					"Northernmost Latitude",
					"Southernmost Latitude",
					"Easternmost Longitude",
					"Westernmost Longitude",
					"Center Latitude",
					"Center Longitude", 
					"Origin of Name"]
	df = pd.DataFrame(feature_options, columns=header_options)
	df = df.sort_values(by=["Feature Name"])
	df.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'feature_name_details.csv'), header=header_options, index=False)

if __name__ == '__main__':
	updateCsvFeatureNameDetails() #	updates feature_name_details.csv
