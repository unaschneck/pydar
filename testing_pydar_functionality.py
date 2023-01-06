import pydar

if __name__ == '__main__':
	# Extract Flyby Data Files to results/ directory
	#pydar.extractFlybyDataImages(flby_id='T65',
	#							resolution='D',
	#							segment_num="S01")

	# Display all Images in results/ directory
	#pydar.displayImages("results/CORADR_0211_V03_S01")
	# TODO: bug fix for 87 displays invalid integer

	# Read AAREADME to console
	pydar.readAAREADME(coradr_results_directory="results/CORADR_0065_V03_S01",
						section_to_print="Volume")

	#pydar.extractMetadata()

