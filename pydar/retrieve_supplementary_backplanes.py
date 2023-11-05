# Extract metadata from SBDR files (.TAB files)
import logging

# External Python libraries (installed via pip install)
import numpy as np
import pdr

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def extractMetadata(isVersionComplete=False):
	# Note: need both the .TAB and the .FMT file to run
	isVersionComplete = False
	if not isVersionComplete:
		raise ValueError("extractMetadata() not available for v1 release")

	tab_file = "pydar/testing_files/SBDR_15_D065_V03.TAB"
	SBDR_FILE = pdr.read(tab_file)
	#logger.info(SBDR_FILE['SBDR_TABLE'])
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

	#logger.info(radar_mode)
	
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
	logger.info('Unique Beam Patterns before filtering: '+str(sbdr_sar['BEM'].unique()))

	# filter SAR data for best active points (Alex's #97)
	# Active Point: active or passive sensor, but only gets when radar when in an active state
	# ACT_AZIMUTH_ANGLE: Direction of the projection of the antenna look vector into the plane 
	#					 tangent the surface at the center of the measurement as an angle CCW from East 
	#					 (such that N is 90 deg)
	# ACT_ELLIPSE_PT1_LAT: Latitude of the first point (on major axis) in the ellipse marking the 
	# 					   active measurement two way 3-dB gain pattern. 
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_AZIMUTH_ANGLE'] != 0]
	sbdr_sar = sbdr_sar[sbdr_sar['ACT_ELLIPSE_PT1_LAT'] != 0]
	
	logger.info('Found {0} active beam pulses in SAR'.format(len(sbdr_sar)))
	# total width of the RADAR swath is created by combining the five individually illuminated subbeams 
	# each bursts use different beam(s) while taking SAR measurements
	beam_1 = [] # DEFINE: Smallest look angle subbeam 
	beam_2 = [] # DEFINE: Second-smallest look angle subbeam
	beam_3 = [] # DEFINE: Middle subbeam swath with greatest gain
	beam_4 = [] # DEFINE: Second-largest look angle subbeam
	beam_5 = [] # DEFINE: Largest look angle subbeam

	logger.info('Unique Beam Patterns used after filtering: '+str(sbdr_sar['BEM'].unique()))
		
		
	for x in sbdr_sar['BEM']:
		binx = bin(x)[2:].zfill(2)
		beam_5.append(binx[0])
		beam_4.append(binx[1])
		beam_3.append(binx[2])
		beam_2.append(binx[3])
		beam_1.append(binx[4])
		
	
	#beam = sbdr_sar['BEM'].tolist()
	#logger.info('size of beam',+len(sbdr_sar['BEM']))
	# convert to integer and sum
	beam_1 = list(map(int, beam_1))
	beam_2 = list(map(int, beam_2))
	beam_3 = list(map(int, beam_3))
	beam_4 = list(map(int, beam_4))
	beam_5 = list(map(int, beam_5))

	logger.info("# of Bursts with Beam 1: "+str(sum(beam_1)))
	logger.info("# of Bursts with Beam 2: "+str(sum(beam_2)))
	logger.info("# of Bursts with Beam 3: "+str(sum(beam_3)))
	logger.info("# of Bursts with Beam 4: "+str(sum(beam_4)))
	logger.info("# of Bursts with Beam 5: "+str(sum(beam_5)))
	logger.info("# of Bursts Total: "+str(len(sbdr_sar['BEM'])))

'''
	#img_file = "pydar_results/CORADR_0211_V03_S01/BIBQD78S004_D211_T065S01_V03.IMG"
	#BIDR_FILE = pdr.read(img_file)
	#logger.info(BIDR_FILE.keys())

	#['.start_burst_num'] and ['.end_burst_num']
'''
