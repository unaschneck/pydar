# Extract metadata from SBDR files (.TAB files)

import numpy as np
import pdr


def extractMetadata():
	tab_file = "pydar_results/CORADR_0211_V03_S01/SBDR_11_D211_V03.TAB"
	SBDR_FILE = pdr.read(tab_file)
	#print(SBDR_FILE['SBDR_TABLE'])
	# Each row is Burst Data
	#print("Headers = {0}".format(list(SBDR_FILE['SBDR_TABLE'])))

	# TODO: Associated Burt Data with Image Data	
	# RADAR_MODE:
	# 	0 or 8 = Scatterometry
	# 	1 or 9 = Altimetry
	#	2 or 10 = Low Res SAR
	# 	3 or 11= High Res SAR
	# 	4 or 12 = Radiometry
	# 	where +8 = Auto-Gain enabled
	radar_mode = SBDR_FILE['SBDR_TABLE']['RADAR_MODE']
	sbdr = SBDR_FILE['SBDR_TABLE']
	#print(radar_mode)
	
	# identify the low and high res sar with and without autogain
	low_res_sar_burst = sbdr.index[sbdr.RADAR_MODE == 3].tolist()
	if len(sbdr.index[sbdr.RADAR_MODE == 11].tolist())>0:
		low_res_sar_burst = low_res_sar_burst + sbdr.index[sbdr.RADAR_MODE == 11].tolist()

	hi_res_sar_burst = sbdr.index[sbdr.RADAR_MODE == 4].tolist()
	if len(sbdr.index[sbdr.RADAR_MODE == 12].tolist())>0:
		hi_res_sar_burst = hi_res_sar_burst + sbdr.index[sbdr.RADAR_MODE == 12].tolist()
	# collect sar data indices into one list
	sar_ind = low_res_sar_burst + hi_res_sar_burst
	sbdr_sar = sbdr.iloc[sar_ind]

	# filter SAR data for best active points (#97)
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_AZIMUTH_ANGLE'] != 0]
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_ELLIPSE_PT1_LAT'] != 0]

	# Create beam mask (1-5 with 3 at center with highest gain)
	BEM = [(x) for x in sbdr_sar['BEM']]
	print(BEM)
	NO_BEAM = int('00000',2)
	print('NO BEAM: {}'.format(NO_BEAM))
	BEAM_1 = int('00001',2)
	print('BEAM 1: {}'.format(BEAM_1))
	BEAM_2 = int('00010',2)
	print('BEAM 2: {}'.format(BEAM_2))
	BEAM_3 = int('00011',2)
	print('BEAM 3: {}'.format(BEAM_3))
	BEAM_4 = int('10000',2)
	print('BEAM 4: {}'.format(BEAM_4))
	BEAM_245 = int('11010',2)
	print('BEAM 245: {}'.format(BEAM_245))
	BEAM_ALL = int('11111',2)
	print('ALL BEAM: {}'.format(BEAM_ALL))

	print(set(list((BEM)))) # unique values in BEM
	
	BEAM_1 = 1
	BEAM_2 = 2
	BEAM_3 = 4
	BEAM_4 = 8
	BEAM_5 = 16
	

	#img_file = "pydar_results/CORADR_0211_V03_S01/BIBQD78S004_D211_T065S01_V03.IMG"
	#BIDR_FILE = pdr.read(img_file)
	#print(BIDR_FILE.keys())

	#['.start_burst_num'] and ['.end_burst_num']


# 
