# Extract metadata from SBDR files (.TAB files)

import pdr

def extractMetadata():
	test_file = "pydar_results/CORADR_0065_V03_S01/SBDR_15_D065_V03.TAB"
	BIDR_FILE = pdr.read(test_file)
	print(BIDR_FILE.keys())
	#print(BIDR_FILE['SBDR_TABLE'])
	# Each row is Burst Data
	print("Headers = {0}".format(list(BIDR_FILE['SBDR_TABLE'])))

	# TODO: Associated Burt Data with Image Data
	img_file = "pydar_results/CORADR_0065_V03_S01/BIBQD10S251_D065_T008S01_V03.IMG"
	SBDR_FILE = pdr.read(img_file)
	#print(SBDR_FILE.keys())

	#['.start_burst_num'] and ['.end_burst_num']
