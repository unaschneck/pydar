# Read AAREADME.TXT and .LBL sections to console
import logging

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

aareadme_options = ["PDS_VERSION_ID",
					"RECORD_TYPE",
					"INSTRUMENT_HOST_NAME",
					"INSTRUMENT_NAME",
					"OBJECT",
					"PUBLICATION_DATE",
					"NOTE",
					"END_OBJECT",
					"Volume",
					"Introduction",
					"Disk Format",
					"File Formats",
					"Volume Contents",
					"Recommended DVD Drives and Driver Software",
					"Errata and Disclaimer",
					"Version Status",
					"Contact Information"
					]

def returnAllAAREADMEOptions():
	logger.info(aareadme_options)

def readAAREADME(coradr_results_directory=None, section_to_print=None, print_to_console=True):
	# Print AAREADME to console
	#logger.info("readme options: {0}\n".format(readme_options))

	# Define position to start console print, default to 'All' if no section is specified
	if section_to_print is None:
		start_index = 0
		start_position = aareadme_options[start_index]
	else:
		start_index = aareadme_options.index(section_to_print)
		start_position = aareadme_options[start_index]

	# Define position to end console print, defaults to end of file if no section is specified
	if section_to_print is None:
		end_index = None
		end_position = None
	else:
		end_index = start_index + 1
		if end_index >= len(aareadme_options): 
			end_position = None # display the last element in the list
		else:
			end_position = aareadme_options[end_index]

	output_string = ''
	with open("{0}/AAREADME.TXT".format(coradr_results_directory), "r") as readme_file:
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
				if print_to_console: 
					output_string += line
	output_string = output_string.rstrip()
	if print_to_console: printToConsole(output_string)
	return output_string

def printToConsole(output_string):
	logger.info(output_string)

def returnAllLBLOptions():
	return

def readLBL(coradr_results_directory=None, section_to_print=None, print_to_console=True):
	# Print .LBL to console
	return
