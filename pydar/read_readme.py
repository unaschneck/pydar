# Read AAREADME.TXT and .LBL sections to console

# Built in Python functions
import logging
import os

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

#######################################################################
# Find relevant section to print by referencing built in options
def determineSectionToPrint(section_to_print=None, aareadmeOrLBL=None):
	# check which list the section_to_print is from
	if aareadmeOrLBL == "LBL":
		if section_to_print in lblreadme_general_options:
			return lblreadme_general_options
		if section_to_print in lblreadme_section_options:
			return lblreadme_section_options
	if aareadmeOrLBL == "AAREADME":
		if section_to_print in aareadme_general_options:
			return aareadme_general_options
		if section_to_print in aareadme_section_options:
			return aareadme_section_options

#######################################################################
## AAREADME.TXT
aareadme_general_options = ["PDS_VERSION_ID",
							"RECORD_TYPE",
							"INSTRUMENT_HOST_NAME",
							"INSTRUMENT_NAME",
							"PUBLICATION_DATE",
							"NOTE",
							"Volume"]
aareadme_section_options = ["Introduction",
							"Disk Format",
							"File Formats",
							"Volume Contents",
							"Recommended DVD Drives and Driver Software",
							"Errata and Disclaimer",
							"Version Status",
							"Contact Information"]

def returnAAREADMEOptions():
	logger.info(f"Line-By-Line Options: {aareadme_general_options}")
	logger.info(f"Section Header Options: {aareadme_section_options}")

def readAAREADME(coradr_results_directory=None, section_to_print=None, print_to_console=True):
	# Print AAREADME to console
	pydar.errorHandlingREADME(coradr_results_directory=coradr_results_directory,
							section_to_print=section_to_print,
							print_to_console=print_to_console)

	sectionList = determineSectionToPrint(section_to_print, "AAREADME")
	if sectionList is None:
		section_to_print = section_to_print.upper() # check if the section is case-sensitive
		sectionList = determineSectionToPrint(section_to_print, "AAREADME")
		if sectionList is None:
			section_to_print = section_to_print.title() # check if the section is case-sensitive
			sectionList = determineSectionToPrint(section_to_print, "AAREADME")
			if sectionList is None:
				raise ValueError(f"[readAAREADME]: Cannot find a revelant section_to_print: Invalid '{section_to_print}'")

	# Define position to start console print, default to 'All' if no section is specified
	if section_to_print is None:
		start_index = 0
		start_position = sectionList[start_index]
	else:
		start_index = sectionList.index(section_to_print)
		start_position = sectionList[start_index]

	# Define position to end console print, defaults to end of file if no section is specified
	if section_to_print is None:
		end_index = None
		end_position = None
	else:
		end_index = start_index + 1
		if end_index >= len(sectionList): 
			if sectionList == aareadme_general_options:
				end_position = aareadme_section_options[0] # the start of the section list is the end of the line-by-line list
			if sectionList == aareadme_section_options:
				end_position = None # display the last element in the list
		else:
			end_position = sectionList[end_index]

	# Find relevant line to print based on the starting text
	if not any("AAREADME.TXT" in sub for sub in os.listdir(coradr_results_directory)):
		raise ValueError(f"'{coradr_results_directory}' does not contain AAREADME.TXT")
	output_string = ''
	with open(f"{coradr_results_directory}/AAREADME.TXT", "r") as readme_file:
		within_readme_section = False
		for line in readme_file.readlines():
			if start_position in line:
				if start_position != "Volume":
					within_readme_section = True
				else:
					if "Titan Flyby T" in line:
						within_readme_section = True
			if end_position is not None:
				if end_position in line:
					if end_position != "Volume":
						break
					else:
						if "Titan Flyby T" in line:
							break
			if within_readme_section:
				if 'OBJECT' not in line and 'END' not in line:
					output_string += line

	output_string = output_string.rstrip() # remove excessive whitespace

	if "=" in output_string and sectionList != aareadme_section_options:
		output_string = (output_string.split("=")[1]).strip() # only return the value from the line (PDS_VERSION_ID       = PDS3 -> PDS3)
	else:
		output_string = output_string.strip() # 'Volume' option display entire row
	if print_to_console: logger.info(output_string)
	return output_string
#########################################################################

#########################################################################
## .LBL README FILES
lblreadme_general_options = ["PDS_VERSION_ID",
							"DATA_SET_ID",
							"DATA_SET_NAME",
							"PRODUCER_INSTITUTION_NAME",
							"PRODUCER_ID",
							"PRODUCER_FULL_NAME",
							"PRODUCT_ID",
							"PRODUCT_VERSION_ID",
							"INSTRUMENT_HOST_NAME",
							"INSTRUMENT_HOST_ID",
							"INSTRUMENT_NAME",
							"INSTRUMENT_ID",
							"TARGET_NAME",
							"START_TIME",
							"STOP_TIME",
							"SPACECRAFT_CLOCK_START_COUNT",
							"SPACECRAFT_CLOCK_STOP_COUNT",
							"PRODUCT_CREATION_TIME",
							"SOURCE_PRODUCT_ID",
							"MISSION_PHASE_NAME",
							"MISSION_NAME",
							"SOFTWARE_VERSION_ID",
							"FILE_NAME COMPRESSED",
							"RECORD_TYPE COMPRESSED",
							"ENCODING_TYPE",
							"INTERCHANGE_FORMAT",
							"UNCOMPRESSED_FILE_NAME",
							"REQUIRED_STORAGE_BYTES",
							"^DESCRIPTION",
							"FILE_NAME UNCOMPRESSED",
							"RECORD_TYPE UNCOMPRESSED",
							"RECORD_BYTES",
							"FILE_RECORDS",
							"LABEL_RECORDS",
							"^IMAGE",
							"LINES",
							"LINE_SAMPLES",
							"SAMPLE_TYPE",
							"SAMPLE_BITS",
							"CHECKSUM",
							"SCALING_FACTOR",
							"OFFSET",
							"MISSING_CONSTANT",
							"NOTE",
							"^DATA_SET_MAP_PROJECTION",
							"MAP_PROJECTION_TYPE",
							"FIRST_STANDARD_PARALLEL",
							"SECOND_STANDARD_PARALLEL",
							"A_AXIS_RADIUS",
							"B_AXIS_RADIUS",
							"C_AXIS_RADIUS",
							"POSITIVE_LONGITUDE_DIRECTION",
							"CENTER_LATITUDE",
							"CENTER_LONGITUDE",
							"REFERENCE_LATITUDE",
							"REFERENCE_LONGITUDE",
							"LINE_FIRST_PIXEL",
							"LINE_LAST_PIXEL",
							"SAMPLE_FIRST_PIXEL",
							"SAMPLE_LAST_PIXEL",
							"MAP_PROJECTION_ROTATION",
							"MAP_RESOLUTION",
							"MAP_SCALE",
							"MAXIMUM_LATITUDE",
							"MINIMUM_LATITUDE",
							"EASTERNMOST_LONGITUDE",
							"WESTERNMOST_LONGITUDE",
							"LINE_PROJECTION_OFFSET",
							"SAMPLE_PROJECTION_OFFSET",
							"OBLIQUE_PROJ_POLE_LATITUDE",
							"OBLIQUE_PROJ_POLE_LONGITUDE",
							"OBLIQUE_PROJ_POLE_ROTATION",
							"OBLIQUE_PROJ_X_AXIS_VECTOR",
							"OBLIQUE_PROJ_Y_AXIS_VECTOR",
							"OBLIQUE_PROJ_Z_AXIS_VECTOR",
							"LOOK_DIRECTION",
							"COORDINATE_SYSTEM_NAME",
							"COORDINATE_SYSTEM_TYPE"]
lblreadme_section_options = ["PRODUCT DESCRIPTION",
							"DESCRIPTION OF COMPRESSED AND UNCOMPRESSED FILES",
							"POINTERS TO START RECORDS OF OBJECTS IN FILE",
							"DESCRIPTION OF OBJECTS CONTAINED IN FILE"]

def returnLBLOptions():
	# Print out all the .LBL options
	logger.info(f"Line-By-Line Options: {lblreadme_general_options}")
	logger.info(f"Section Header Options: {lblreadme_section_options}")

def readLBLREADME(coradr_results_directory=None, section_to_print=None, print_to_console=True):
	# Print .LBL to console
	if section_to_print == "FILE_NAME" or section_to_print == "RECORD_TYPE":
		# Same text used to reference both FILE_NAME and RECORD_TYPE, user needs to specify if UNCOMPRESSED or COMPRESSED file
		raise ValueError(f"Specify {section_to_print} as either '{section_to_print} UNCOMPRESSED' or '{section_to_print} COMPRESSED'")
	# Catch common misspelling: not including the ^ at the front of a line name
	if section_to_print == "DESCRIPTION" or section_to_print == "IMAGE" or section_to_print == "DATA_SET_MAP_PROJECTION":
		section_to_print = f"^{section_to_print}" # sets the user's option to include the easy to miss ^

	pydar.errorHandlingREADME(coradr_results_directory=coradr_results_directory,
							section_to_print=section_to_print,
							print_to_console=print_to_console)

	sectionList = determineSectionToPrint(section_to_print, "LBL")
	if sectionList is None:
		# check if the section is case-sensitive
		section_to_print = section_to_print.upper()
		sectionList = determineSectionToPrint(section_to_print, "LBL")
		if sectionList is None:
			raise ValueError(f"[readLBLREADME]: Cannot find a revelant section_to_print: Invalid '{section_to_print}'")

	# Define position to start console print, default to 'All' if no section is specified
	if section_to_print is None:
		start_index = 0
		start_position = sectionList[start_index]
	else:
		start_index = sectionList.index(section_to_print)
		start_position = sectionList[start_index]
	if "FILE_NAME " in section_to_print or "RECORD_TYPE " in section_to_print:
		# two repeated types, get the files before the repeated option
		if "COMPRESSED" in section_to_print:
			start_index = sectionList.index("SOFTWARE_VERSION_ID")
			start_position = sectionList[start_index]
		if "UNCOMPRESSED" in section_to_print:
			start_index = sectionList.index("REQUIRED_STORAGE_BYTES")
			start_position = sectionList[start_index]

	# Define position to end console print, defaults to end of file if no section is specified
	if section_to_print is None:
		end_index = None
		end_position = None
	else:
		end_index = start_index + 1
		if end_index >= len(sectionList): 
			end_position = None # display the last element in the list
		else:
			end_position = sectionList[end_index]
	if "FILE_NAME " in section_to_print or "RECORD_TYPE " in section_to_print:
		# two repeated types, get the files before the repeated option
		if "COMPRESSED" in section_to_print:
			end_index = sectionList.index("INTERCHANGE_FORMAT")
			end_position = sectionList[end_index]
		if "UNCOMPRESSED" in section_to_print:
			end_index = sectionList.index("FILE_RECORDS")
			end_position = sectionList[end_index]

	output_string = ''
	lbl_file = [i for i in os.listdir(coradr_results_directory) if '.LBL' in i]
	if len(lbl_file) != 1:
		# error handling to check that .LBL exists
		if len(lbl_file) == 0:
			# No .LBL files found
			raise ValueError(f"No .LBL file found at {coradr_results_directory}")
		if len(lbl_file) > 1:
			# Multiple .LBL files found
			raise ValueError(f"Multiple .LBL file found = {lbl_file}, need to choose one to read from")

	lbl_file = lbl_file[0] # set to the LBL file, without extension

	output_string = ''
	with open(f"{coradr_results_directory}/{lbl_file}", "r") as readme_file:
		within_readme_section = False
		for line in readme_file.readlines():
			if start_position in line:
				within_readme_section = True
			if end_position is not None:
				if end_position in line:
					break
			if within_readme_section:
				if sectionList is not lblreadme_section_options:
					if "/*" not in line: # if checking individual values, ignore /**/ section headers
						output_string += line
					else:
						if "FILE_NAME " not in section_to_print and "RECORD_TYPE " not in section_to_print:
							break
				else:
					output_string += line # collection by section

	repeated_or_skipped_values_to_find = ["FILE_NAME", "RECORD_TYPE", "^DESCRIPTION", "COORDINATE_SYSTEM_TYPE"]
	output_lines = output_string.split("\n")
	if section_to_print.split(" ")[0] in repeated_or_skipped_values_to_find:
		for line in output_lines:
			if section_to_print.split(" ")[0] in line:
				output_string = line
	
	if section_to_print == "NOTE":
		output_string = ""
		for line in output_lines:
			if "END_OBJECT" not in line:
				output_string += " " + line.strip() + " " # fix additional tabs added in text file by stripping out
			else:
				break

	output_string = output_string.rstrip() # remove excessive whitespace

	if sectionList != lblreadme_section_options:
		output_string = (output_string.split("=")[1]).strip() # only return the value from the line (PDS_VERSION_ID       = PDS3 -> PDS3)
	if print_to_console: logger.info(output_string)
	return output_string
########################################################################
