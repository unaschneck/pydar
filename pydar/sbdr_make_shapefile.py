# Script to generate an ARC Shape File from SBDR Table Data

# Built in Python functions
import time
import logging
import math

# External Python libraries (installed via pip install)
import numpy as np
import pandas as pd
import pdr

# Internal Pydar reference to access functions, global variables, and error handling
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
						file_out=None, 
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

	# Set Filename default is filename is not characters: (TODO: does this need to be included?")
	#if not filename.isalpha():
	#	info = filename
	#	filename = "DefaultFile.sbdr"
	logger.debug("Reading {0} ...".format(filename))
	info = pdr.read(filename)
	info = info['SBDR_TABLE']
	logger.debug("Headers = {0}\n".format(list(info)))
	#print(info['ACT_POL_ANGLE'])

	# Define the Titan Ellipsoid
	r_titan = 2575000 # radius in meters
	flat_titan = 0
	titan_def = [r_titan/1000 , flat_titan] # [radius in km, 0]

	# Create Output Filename
	if file_out is None:
		file_out = filename.split(".")[0] + ".shp"
		file_out2 = filename.split(".")[0] + "_centroid.shp"
		file_out3 = filename.split(".")[0] + "_center.shp"
	else:
		file_out = file_out + ".shp"
		file_out2 = file_out + "_centroid.shp"
		file_out3 = file_out + "_center.shp"
	logger.debug("Filenames for Output:\n{0}\n{1}\n{2}".format(file_out, file_out2, file_out3))

	# Filtering based on SAR and Active/Passive Radar
	# Find the Good Active Points (Usable data with low distortion from spacecraft orientation)
	if saronly >= 0: # if not just looking at SAR data, get the radarmode from the data
		r = info.RADAR_MODE
		if saronly == 2: # Get the Low Res SAR data
			if usepassive: # Passive Radar
				# Find all indices of data that are high rest SAR data and the azimuth angle and highest(?) latitude of the ellipse is not zero
				ind = info[info.RADAR_MODE.isin([3, 11])]
				ind = ind[~ind.ACT_AZIMUTH_ANGLE.isin([0])]
				ind = ind[~ind.PASS_ELLIPSE_PT1_LAT.isin([0])]
			else: # Active Radar
				ind = info[info.RADAR_MODE.isin([3, 11])]
				ind = ind[~ind.ACT_AZIMUTH_ANGLE.isin([0])]
				ind = ind[~ind.ACT_ELLIPSE_PT1_LAT.isin([0])]
		elif saronly == 3: # High Res SAR
			ind = info[~info.PASS_ELLIPSE_PT1_LAT.isin([0])]
			ind = ind[~ind.SAR_RANGE_RES.isin([0])]
			ind = ind[~ind.ACT_MAJOR_WIDTH.isin([0])]
		else: # If not 2 or 3
			if usepassive:
				ind = info[~info.PASS_ELLIPSE_PT1_LAT.isin([0])]
				ind = ind[~ind.SAR_RANGE_RES.isin([0])]
				ind = ind[~ind.SAR_AZIMUTH_RES.isin([0])]
			else:
				# TODO: note: usepassive and not use the same functionality
				ind = info[~info.PASS_ELLIPSE_PT1_LAT.isin([0])]
				ind = ind[~ind.SAR_RANGE_RES.isin([0])]
				ind = ind[~ind.SAR_AZIMUTH_RES.isin([0])]

		if len(ind.index) == 0: # No data  satifies all conditions
			ind = info[~info.ACT_AZIMUTH_ANGLE.isin([0])]
			ind = ind[~ind.ACT_ELLIPSE_PT1_LAT.isin([0])]
			logger.info("ERROR: No Active SAR Model")
			struct = []
			return
		else:
			logger.info("Found {0} Active Pulses".format(len(ind.index)))
	else:
		ind = info[~info.ACT_AZIMUTH_ANGLE.isin([0])]
		ind = ind[~ind.ACT_ELLIPSE_PT1_LAT.isin([0])]
	
	num_record = len(ind.index) # Number of good data

	# Get the Required Data
	ind_lst = ind.index.values.tolist() # index of all valid points
	if usepassive:
		act_pt1_lat = info.iloc[ind_lst].PASS_ELLIPSE_PT1_LAT
		act_pt2_lat = info.iloc[ind_lst].PASS_ELLIPSE_PT2_LAT
		act_pt3_lat = info.iloc[ind_lst].PASS_ELLIPSE_PT3_LAT
		act_pt4_lat = info.iloc[ind_lst].PASS_ELLIPSE_PT3_LAT
		
		act_pt1_lon = info.iloc[ind_lst].PASS_ELLIPSE_PT1_LON
		act_pt2_lon = info.iloc[ind_lst].PASS_ELLIPSE_PT2_LON
		act_pt3_lon = info.iloc[ind_lst].PASS_ELLIPSE_PT3_LON
		act_pt4_lon = info.iloc[ind_lst].PASS_ELLIPSE_PT4_LON
		
		act_min_wid = info.iloc[ind_lst].PASS_MINOR_WIDTH
		act_maj_wid = info.iloc[ind_lst].PASS_MINOR_WIDTH
		act_cen_lat = info.iloc[ind_lst].PASS_CENTROID_LAT
		act_cen_lon = info.iloc[ind_lst].PASS_CENTROID_LON
		act_az = info.iloc[ind_lst].ACT_AZIMUTH_ANGLE
	else:
		act_pt1_lat = info.iloc[ind_lst].ACT_ELLIPSE_PT1_LAT
		act_pt2_lat = info.iloc[ind_lst].ACT_ELLIPSE_PT2_LAT
		act_pt3_lat = info.iloc[ind_lst].ACT_ELLIPSE_PT3_LAT
		act_pt4_lat = info.iloc[ind_lst].ACT_ELLIPSE_PT3_LAT
		
		act_pt1_lon = info.iloc[ind_lst].ACT_ELLIPSE_PT1_LON
		act_pt2_lon = info.iloc[ind_lst].ACT_ELLIPSE_PT2_LON
		act_pt3_lon = info.iloc[ind_lst].ACT_ELLIPSE_PT3_LON
		act_pt4_lon = info.iloc[ind_lst].ACT_ELLIPSE_PT4_LON
		
		act_min_wid = info.iloc[ind_lst].ACT_MINOR_WIDTH
		act_maj_wid = info.iloc[ind_lst].ACT_MINOR_WIDTH
		act_cen_lat = info.iloc[ind_lst].ACT_CENTROID_LAT
		act_cen_lon = info.iloc[ind_lst].ACT_CENTROID_LON
		act_az = info.iloc[ind_lst].ACT_AZIMUTH_ANGLE

	if saronly == 3:
		min_wid = info.iloc[ind_lst].ACT_MINOR_WIDTH
		maj_wid = info.iloc[ind_lst].ACT_MAJOR_WIDTH

	def azimuth(lat1, lat2, long1, long2, radius):
		# convert decimal degrees to radians 
		long1, lat1, long2, lat2 = map(math.radians, [long1, lat1, long2, lat2])
		
		diff_lats = lat2 - lat1
		diff_long = long2 - long1
		a = math.sin(diff_lats/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_long/2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		az = c * radius
		return az


	# Loop through Data fields
	cnt = 1
	gfields = {}
	for field in fields:
		if field.upper() in list(info): # checks that field is an element in the info dataframe 
			gfields[cnt] = field # Convert matlab structure to dict
			cnt += 1
		else:
			logger.info("{0} Not a Valid Field!".format(field))
	if cnt == 1: # If the fields are not moved through, then no fields are returned
		logger.info("No Valid Fields Returning...")
		return

	# Progress Bar: Print an update to the screen
	# TODO: Currently does nothing
	#eta_start = time.time()
	#for num in range(num_record):
	#	if num < num_record:
	#		print("{0} of {1} ({2} Percent Complete".format(num+1, num_record, num+1/num_record), end="\r")
	#print("") # reset printing to terminal

	# Step through each footprint and create 100 latitude/longitude points around the ellipse to create a perimeter
	for i in range(num_record): # TODO: check if i should be the index or the value?
		# TODO: num_record + 1? to get all?
		# 1 to all valid data points
		# Get the ellipse center and semi-major axis, eccentricity, and azimuth
		pt1x = float(act_pt1_lat.iloc[[i]])
		pt1y = float(act_pt1_lon.iloc[[i]])
		pt2x = float(act_pt2_lat.iloc[[i]])
		pt2y = float(act_pt2_lon.iloc[[i]])
		pt3x = float(act_pt3_lat.iloc[[i]])
		pt3y = float(act_pt3_lon.iloc[[i]])
		pt4x = float(act_pt4_lat.iloc[[i]])
		pt4y = float(act_pt4_lon.iloc[[i]])
		ptx = [pt1x, pt2x, pt3x, pt4x] # TODO: duplicate of below line, remove?
		pty = [pt1y, pt2y, pt3y, pt4y]

		# Convert lons into -180 to 180
		if pt1y > 180: pt1y = pt1y - 360
		if pt2y > 180: pt2y = pt2y - 360
		if pt3y > 180: pt3y = pt3y - 360
		if pt4y > 180: pt4y = pt4y - 360
		if pt1y < -180: pt1y = pt1y + 360
		if pt2y < -180: pt2y = pt2y + 360
		if pt3y < -180: pt3y = pt3y + 360
		if pt4y < -180: pt4y = pt4y + 360

		ptx = [pt1x, pt2x, pt3x, pt4x] # Latitudes
		pty = [-x for x in pty] # Convert Longitudes to negative

		# Check if Crosses 180 or 360
		if (min([abs(i) - 360 for i in pty]) < 2) or (min([abs(i) for i in pty]) < 2):
			# Convert to -180 or 180
			for i, pt in enumerate(pty):
				if pt > 180:
					pty[i] = pt - 360 # TODO: verify: pty(pty > 180) = pty(pty > 180) -360
		elif (min([abs(i) - -180 for i in pty]) < 2):
			# Convert between 0 and 360
			for i, pt in enumerate(pty):
				if pt < 0:
					pty[i] = pt + 360 # TODO: verify: pty(pty < 0) = pty(pty < 0) + 360

		# If lon360, convert to between 0 and 360
		if lon360:
			for i, pt in enumerate(pty):
				if pt < 0:
					pty[i] = pt + 360 # TODO: verify: pty(pty < 0) = pty(pty < 0) + 360

		# Ensure that single records exist
		pt1y = pty[0]
		pt2y = pty[1]
		pt3y = pty[2]
		pt4y = pty[3]
		pt1x = ptx[0]
		pt2x = ptx[1]
		pt3x = ptx[2]
		pt4x = ptx[3]

		# Set azimuth for intersecton of ellipsis
		print(azimuth(pt1x, pt2x, pt1y, pt2y, titan_def[0]))
		exit()
		gc_az1 = azimuth([pt1x, pt1y], [pt2x, pt2y], titan_def)
		gc_az2 = azimuth([pt3x, pt3x], [pt4x, pt4y], titan_def)

		"""
		# Calculate the intersection point
		[lat0, lon0] = gcxgc(pt1x, pt1y ,gc_az1 ,pt3x ,pt3y ,gc_az2)

		# Use intersection point that is within the elipse
		dist1 = distanc(pt1x, pt1y, lat0[0], lon0[0])
		dist2 = distance(pt1x, pt1y, lat0[1], lon0[1])

		if dist1 < dist2:
			lat0 = lat0[0]
			lon0 = lon0[0]
		else: # use interaction with a flat surface
			lat0 = lat0[1]
			lon0 = lon0[1]

		if lon0 < -180:
			lon0 += 360
		if lon0 > 180:
			lon0 -= 360
		lat0s[i] = lat0
		lon0s[i] = lon0

		# Center of elipse
		latcens[i] = act_cent_lat[i]
		loncens[i] = -act_cen_long[i]
		if loncens[i] < 180:
			loncens[i] += 360
		if loncens[i] > 180:
			loncens[i] -= 360
		if ( (abs(lon0 - loncens[i]) < 4 ): # Check if crosses 180 or 360
			lat0 = -lat0
		if ( (abs(lon0 - loncens[i]) > 4 ): # Check if crosses 180 or 360
			lon0 -= 180
		if lon0 < -180: # Convert between -180 to 180
			lon0 += 360 
		if lon0 > 180: # Convert between -180 to 180
			lon0 += 360
		if lon0 > 180: # Convert between -180 to 180
			lon0 -= 360

		# Converting back to 0 to 360
		if lon360:
			for i, lon in lon0:
				if lon < 0:
					lon0[i] = lon + 360
			for i, lon in lon0s:
				if lon < 0:
					lon0s[i] = lon + 350
			for i, lon in loncens:
				if lon < 0:
					loncens[i] = lon + 360

		# Calculate the Ellipse
		minor = act_min_wid[i]
		major = act_maj_wid[i]

		# Defining the eccentricity of ellipse
		if major == 0 or minor == 0:
			ecc = 0
		else:
			ecc = math.sqrt( 1 - (minor/major)**2)

		[lat, lon] = ellipse1(latcens[i], loncens[i], (major/ 2 * ecc), gc_az1, [], titan_def)

		# Get the reported azimutal look direction
		az = -1 * act_az[i]

		# Convert the longitude values into -180 to 180
		for i, l in enumerate(lon):
			if l > 180:
				lon[i] = l -360
		for i, l in enumerate(lon0s):
			if l > 180:
				lon0s[i] = l - 360
		for i, l in enumerate(loncens):
			if l > 180:
				loncens[i] = l - 360

		# If passes through 180 in the middle, fix it
		if (max(lon) > 170) and min(lon) < -170)):
			for i, l in enumerate(lon):
				if l < 0:
					lon[i] = lon + 360

		# Center the ellipse on pt1 (top of ellipse)
		# Minimum between top of ellipse and lat and long of perimeter of ellipse
		[trash, minind] = min( math.sqrt( (pt1x - lat)**2 + (pt1y - lon)**2 ) )
		latoff1 = pt1x - lat(minind)
		lonoff1 = pt1y - lon(minind)
		[trash,minind] = min(math.sqrt( (pt2x - lat)**2 + (pt2y - lon)**2 ) );
		latoff2 = pt2x - lat(minind)
		lonoff2 = pt2y - lon(minind)
		[trash,minind] = min( sqrt( (pt3x - lat)**2 + (pt3y - lon)**2 ) );
		latoff3 = pt3x - lat(minind)
		lonoff3 = pt3y - lon(minind)
		[trash,minind] = min( sqrt( (pt4x - lat)**2 + (pt4y - lon)**2 ) );
		latoff4 = pt4x - lat(minind)
		lonoff4 = pt4y - lon(minind)

		latoff = mean([latoff1,latoff2,latoff3,latoff4]) # mean of offsets in lat
		lonoff = mean([lonoff1,lonoff2,lonoff3,lonoff4]) # mean of offesets in lon

		lat = lat + latoff
		lon = lon + lonoff
		"""
