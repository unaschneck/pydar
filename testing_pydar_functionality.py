import pydar

if __name__ == '__main__':
	# Get swatch coverage based on latitude/longitude, Time, or Feature
	flyby_ids_name = pydar.retrieveIDSByFeature(feature_name="Ontario Lacus")
	print("Flyby IDS based on Feature Name = {0}".format(flyby_ids_name))
	flyby_ids_with_segments = pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=177, degrees_of_error=21)
	print("Flyby IDS based on Latitude/Longitude = {0}".format(flyby_ids_with_segments))
	#flyby_ids_time = pydar.retrieveIDSByTime(timestamp="testing")
	#print("Flyby IDS based on Time = {0}".format(flyby_ids_time))

	# Bug: 

	# Convert Flby Id into an Observation Number
	observation_num = pydar.convertFlybyIDToObservationNumber(flyby_id='T65')
	print(observation_num)
	exit()
	# Extract Flyby Data Files to results/ directory
	pydar.extractFlybyDataImages(flyby_id='T43',
								resolution='D',
								segment_num="S01",
								additional_data_types_to_download=["LBDR"])

	# Display all Images in pydar_results/ directory
	#pydar.displayImages(image_directory="pydar_results/CORADR_0211_V03_S01")
	# TODO: bug fix for 87 displays invalid integer

	# Read AAREADME to console
	#pydar.returnAllAAREADMEOptions()
	#pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
	#					section_to_print="INSTRUMENT_NAME")

	# Read .LBL to console
	#pydar.returnAllLBLOptions()
	#pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01/",
	#					section_to_print="LOOK_DIRECTION")

	#pydar.extractMetadata()
