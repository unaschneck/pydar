import pydar

if __name__ == '__main__':
	## Get swatch coverage based on latitude/longitude, Time, or Feature
	#feature_name = "ontario lAcus"
	#flyby_ids_name = pydar.retrieveIDSByFeatureName(feature_name=feature_name)
	#print("Flyby IDS based on Feature Name '{0}' = {1}\n".format(feature_name.title(), flyby_ids_name))

	#flyby_ids_with_segments = pydar.retrieveIDSByLatitudeLongitude(latitude=10, longitude=10)
	#print("Flyby IDS based on Latitude/Longitude = {0}\n".format(flyby_ids_with_segments))

	#flyby_ids_range = pydar.retrieveIDSByLatitudeLongitudeRange(southernmost_latitude=19,
	#															northernmost_latitude=30,
	#															westernmost_longitude=130,
	#															easternmost_longitude=140)
	#print("Flyby IDS based on Latitude/Longitude Range = {0}\n".format(flyby_ids_range))

	#flyby_ids_range = pydar.retrieveIDSByLatitudeLongitudeRange(southernmost_latitude=19,
	#															northernmost_latitude=30,
	#															westernmost_longitude=130,
	#															easternmost_longitude=340)
	#print("Flyby IDS based on Exapnded Latitude/Longitude Range = {0}\n".format(flyby_ids_range))

	#feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitude(latitude=-72, longitude=183)
	#print("Feature Names Found at -72 latitude and 183 longitude = {0}\n".format(feature_names_list))

	#feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitudeRange(southernmost_latitude=-80,
	#																	northernmost_latitude=-50,
	#																	westernmost_longitude=170,
	#																	easternmost_longitude=190)
	#print("Feature Names Found in Latitude/Longitude Range = {0}".format(feature_names_list))

	#flyby_ids_time = pydar.retrieveIDSByTime(year=2001, doy=301)
	#print("Flyby IDS based on a specific timestamp = {0}".format(flyby_ids_time))

	#flyby_ids_time_range = pydar.retrieveIDSByTimeRange(start_year=2004, start_doy=299, start_hour=2, start_minute=15, start_second=23, start_millisecond=987,
	#													end_year=2004, end_doy=299, end_hour=2, end_minute=15, end_second=23, end_millisecond=987)
	#print("Flyby IDS based on a range of timestamps = {0}".format(flyby_ids_time_range))

	# Convert Flby Id into an Observation Number
	#observation_num = pydar.convertFlybyIDToObservationNumber(flyby_id='T65')
	#print(observation_num)

	# Extract Flyby Data Files to results/ directory
	#pydar.extractFlybyDataImages(flyby_id='T43',
	#							resolution='D',
	#							segment_num="S01",
	#							additional_data_types_to_download=["LBDR"])

	# Display all Images in pydar_results/ directory
	#pydar.displayImages(image_directory="pydar_results/CORADR_0211_V03_S01")
	# TODO: bug fix for 87 displays invalid integer

	# Read AAREADME to console
	#pydar.returnAllAAREADMEOptions()
	#pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
	#					section_to_print="INSTRUMENT_name")

	# Read .LBL to console
	#pydar.returnAllLBLOptions()
	#pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01/",
	#					section_to_print="note")
	#pydar.extractMetadata()

	# SBDR Shapefile
	pydar.sbdrMakeShapeFile(filename="pydar/testing_files/SBDR_15_D065_V03.TAB", saronly=3, usepassive=False)
