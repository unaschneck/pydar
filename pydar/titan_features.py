#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      titan_features.py returns Titan features information                                       #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - titan_season: return the season on Titan                #
#                                              based on date                                      #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
from datetime import datetime

# Internal Local Imports
import pydar

########################################################################
def titan_season(hemisphere="north",
				year: str=None,
				month: str=None,
				day: str=None) -> str:
	# returns which season it is on Titan based on date
	# determines the current season on Titan (Northern Hemisphere) given a datetime in Earth time

	# TODO: add in pydar testing

	hemisphere = hemisphere.lower()

	# Titan's northern vernal equinox
	# Source: The evolution of Titan's detached haze layer near equinox in 2009 (West, et al, 2011)
	# https://doi.org/10.1029/2011GL046843
	ref_date = datetime.strptime("2008-08-11", "%Y-%m-%d")

	# Titan Year (in Earth yers)
	titan_year = 29.5 # years
	titan_season_length = titan_year / 4

	# convert date to datetime object
	input_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

	# Calculate elapsed Earth years since reference date
	elapsed_time = input_date - ref_date
	total_time = elapsed_time.days + elapsed_time.seconds + elapsed_time.microseconds
	years_elapsed = total_time / 365.25

	# Determine equivalent Titan year fraction
	titan_year_position = years_elapsed % titan_year

	# Determine the season
	if titan_year_position < titan_season_length:
		season = "Spring"
		if hemisphere == "south":
			season = "Autumn"
	elif titan_year_position < (2 * titan_season_length):
		season = "Summer"
		if hemisphere == "south":
			season = "Winter"
	elif titan_year_position < (3 * titan_season_length):
		season = "Autumn"
		if hemisphere == "south":
			season = "Spring"
	else:
		season = "Winter"
		if hemisphere == "south":
			season = "Summer"

	return season
