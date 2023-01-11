# Extract metadata from SBDR files (.TAB files)
import numpy as np
import pdr

def extractMetadata():
	# Note: need both the .TAB and the .FMT file to run
	
	tab_file = "pydar/testing_files/SBDR_15_D065_V03.TAB"
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
	if len(sbdr.index[sbdr.RADAR_MODE == 11].tolist()) > 0:
		low_res_sar_burst = low_res_sar_burst + sbdr.index[sbdr.RADAR_MODE == 11].tolist()

	hi_res_sar_burst = sbdr.index[sbdr.RADAR_MODE == 4].tolist()
	if len(sbdr.index[sbdr.RADAR_MODE == 12].tolist()) > 0:
		hi_res_sar_burst = hi_res_sar_burst + sbdr.index[sbdr.RADAR_MODE == 12].tolist()

	# collect sar data indices into one list
	sar_ind = low_res_sar_burst + hi_res_sar_burst
	sbdr_sar = sbdr.iloc[sar_ind]

	# filter SAR data for best active points (#97)
	# Active Point: active or passive sensor, but only gets when radar when in an active state
	# ACT_AZIMUTH_ANGLE: [DEFINE]
	# ACT_ELLIPSE_PT1_LAT: [DEFINE]
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_AZIMUTH_ANGLE'] != 0]
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_ELLIPSE_PT1_LAT'] != 0]
	
	print('Found {0} active beam pulses in SAR'.format(len(sbdr_sar)))

	beam_1 = [] # DEFINE:
	beam_2 = [] # DEFINE:
	beam_3 = [] # DEFINE:
	beam_4 = [] # DEFINE:
	beam_5 = [] # DEFINE: 
	for x in sbdr_sar['BEM']:
		bin_beam = str(bin(x))
		beam_5.append(bin_beam[0])
		beam_4.append(bin_beam[1])
		beam_3.append(bin_beam[2])
		beam_2.append(bin_beam[3])
		beam_1.append(bin_beam[4])

	beam = sbdr_sar['BEM'].tolist()

	mask_1 = [beam_1[i]*beam[i] for i in range(len(beam_5))]
	print(beam_1[0])
	print(beam[0])
	print(mask_1[0])

	#img_file = "pydar_results/CORADR_0211_V03_S01/BIBQD78S004_D211_T065S01_V03.IMG"
	#BIDR_FILE = pdr.read(img_file)
	#print(BIDR_FILE.keys())

	#['.start_burst_num'] and ['.end_burst_num']
