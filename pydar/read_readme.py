# Read AAREADME.TXT to command line
import logging

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def readAAREADME(coradr_results_directory):
	# Print AAREADME to command line
	line_limiter = 25 # TODO: set line limit by user, or print by section
	with open("{0}/AAREADME.TXT".format(coradr_results_directory), "r") as readme_file:
		for i, line in enumerate(readme_file.readlines()):
			if i < line_limiter:
				logger.info(line)
		logger.info("... [LINE LIMIT SET TO = {0}]".format(line_limiter))
