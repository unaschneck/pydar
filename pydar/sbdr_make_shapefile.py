# Script to generate an ARC Shape File from SBDR Table Data
import time
import logging

import pydar

## Logging set up for .DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


field_options = ["act_pol_angle",
				"act_incidence_angle",
				"act_azimuth_angle",
				"burst_id",
				"sar_azimuth_res",
				"sar_range_res",
				"sigma0_corrected",
				"sigma0_uncorrected",
				"sigma0_uncorrected_std"]

def sbdrMakeShapeFile(filename=None, 
						fields=[],
						write_files=False,
						saronly=0, 
						usepassive=False, 
						ind=None, 
						file_out=[], 
						lon360=False):
	# filename: name of the SPDR file (string)
	# fields: all burst data if you don't specify (list)
	# write_files : should you create a shp file? (boolean)
	# saronly: what sar data you will take out (conditional statements)
	# usepassive : include passive radar data (boolean)
	# ind : indexes of burst data (list)
	# file_out : name of file output (string)
	# lon360: using 360 Longitude system (boolean) (false = not using, true = using)

	pydar.errorHandlingSbdrMakeShapeFile(filename=filename,
										fields=fields,
										write_files=write_files,
										saronly=saronly,
										usepassive=usepassive,
										ind=ind,
										file_out=file_out,
										lon360=lon360)

	start = time.time()

	# If fields are empty: set to all possible data fields
	if len(fields) == 0:
		fields = field_options

	# saroly defaults to getting all data, not just sar (saronly = 0)
	if saronly == 0: logger.debug("All data, not just SAR")
	if saronly == 1: logger.debug("Using SAR+HiSAR")
	if saronly == 2: logger.debug("Only Using High Resolution SAR Data")
	if saronly == 3: logger.debug("Using SAR + Scatterometry")

	# lon360 is False, default behavior: defined from -180 to 180
	# lon360 is True: defined from 0 to 360
	if lon360: logger.debug("Longitude system: -180 to 180")
	if not lon360: logger.debug("Using 360 Longitude System! (0-360)")

	return
