import pydar

if __name__ == '__main__':
	# Get swatch coverage based on latitude/longitude or Feature
	#pydar.getSwatchCoverageIDS()
	# Extract Flyby Data Files to results/ directory
	#pydar.extractFlybyDataImages(flyby_id='T65',
								#resolution='D',
								#segment_num="S01",
								#additional_data_types_to_download=["STDR", "LBDR"])

	# Display all Images in pydar_results/ directory
	#pydar.displayImages("pydar_results/CORADR_0211_V03_S01")
	# TODO: bug fix for 87 displays invalid integer

	# Read AAREADME to console
	#pydar.returnAllAAREADMEOptions()
	#pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
	#					section_to_print="Volume")

	# Read .LBL to console
	#pydar.returnAllLBLOptions()
	#pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
	#					section_to_print="OBLIQUE_PROJ_X_AXIS_VECTOR")

	pydar.extractMetadata()

