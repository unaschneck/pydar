import pydar

if __name__ == '__main__':
	# Get swatch coverage based on latitude/longitude or Feature
	#pydar.getSwatchCoverageIDS()

	# Convert Flby Id into an Observation Number
	#observation_num = pydar.convertFlybyIDToObservationNumber(flyby_id='T6')

	# Extract Flyby Data Files to results/ directory
	#pydar.extractFlybyDataImages(flyby_observation_num='101',
	#							resolution='I',
	#							segment_num="S01",
	#							additional_data_types_to_download=["LBDR"])

	# Display all Images in pydar_results/ directory
	#pydar.displayImages(image_directory="pydar_results/CORADR_0211_V03_S01")
	# TODO: bug fix for 87 displays invalid integerc

	# Read AAREADME to console
	#pydar.returnAllAAREADMEOptions()
	#pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
	#					section_to_print="Introduction")

	# Read .LBL to console
	#pydar.returnAllLBLOptions()
	pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
						section_to_print="MAXIMUM_LATITUDE")

	#pydar.extractMetadata()
