########################################################################
# ERROR CATCHES AND LOGGING
########################################################################
import logging

import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def errorHandling(flyby_observation_num=None,
				flyby_id=None,
				segment_num=None,
				resolution=None,
				top_x_resolutions=None):
	# Error Handling for extract_flyby_parameters variables
	avaliable_flyby_id, avaliable_observation_numbers = pydar.getFlybyData()

	if flyby_observation_num is None and flyby_id is None:
		logger.critical("\nCRITICAL ERROR: Requires either a flyby_observation_num OR flyby_id.\nAvaliable flyby_observation_num: {0}\nAvaliable flyby_id: {1}".format(avaliable_flyby_id, avaliable_observation_numbers))
		exit()

	if flyby_id is not None:
		if type(flyby_id) != str:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(type(flyby_id)))
			exit()
		if flyby_id not in avaliable_flyby_id:
			logger.critical("\nCRITICAL ERROR, [flyby_id]: '{0}' not in avaliable ids options '{1}'".format(flyby_id, avaliable_flyby_id))
			exit()

	if flyby_observation_num is not None:
		if type(flyby_observation_num) != str:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(type(flyby_observation_num)))
			exit()
		if flyby_observation_num not in avaliable_observation_numbers:
			logger.critical("\nCRITICAL ERROR, [flyby_observation_num]: '{0}' not in avaliable observation options '{1}'".format(flyby_observation_num, avaliable_observation_numbers))
			exit()

	segement_options = ['S01', 'S02', 'S03']
	if segment_num is None:
		logger.critical("\nCRITICAL ERROR, [segment_num]: segment_num number required out of avaliable options {0}, none given".format(segement_options))
		exit()
	if type(segment_num) != str:
		logger.critical("\nCRITICAL ERROR, [segment_num]: Must be a str, current type = '{0}'".format(type(segment_num)))
		exit()
	if segment_num not in segement_options:
		logger.critical("\nCRITICAL ERROR, [segment_num]: '{0}' not an avaliable segment option '{1}'".format(segment_num, segement_options))
		exit()

	if resolution is not None and top_x_resolutions is not None:
		logger.critical("\nCRITICAL ERROR: Requires either a resolution OR a top_x_resolutions, not both".format(type(resolution)))
		exit()

	if resolution is not None :
		if type(resolution) != str:
			logger.critical("\nCRITICAL ERROR, [resolution]: Must be a str, current type = '{0}'".format(type(resolution)))
			exit()
		if resolution not in pydar.resolution_types:
			logger.critical("\nCRITICAL ERROR, [resolution]: resolution '{0}' must be a valid resolution type in {1}".format(resolution, pydar.resolution_types))
			exit()

	if top_x_resolutions is not None:
		if type(top_x_resolutions) != int:
			logger.critical("\nCRITICAL ERROR, [top_x_resolutions]: Must be a int, current type = '{0}'".format(type(top_x_resolutions)))
			exit()
		if top_x_resolutions < 1 or top_x_resolutions > 5:
			logger.critical("\nCRITICAL ERROR, [top_x_resolutions]: Must be a value from 1 to 5, not '{0}'".format(top_x_resolutions))
			exit()
