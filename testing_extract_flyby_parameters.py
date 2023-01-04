import pydar

if __name__ == '__main__':
	# Extract Flyby Data Files to results/ directory
	pydar.extractFlybyDataImages(flyby_observation_num='87',
								resolution='H',
								segment_num="S01")
	# Display all Images in results/ directory
	pydar.displayImages("results/CORADR_0065_V03_S01")
	#pydar.extractMetadata()
