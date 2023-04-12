# Pytest for extract_flyby_parameters.py
# pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys
import logging

# External Python libraries (installed via pip install)
import pytest

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

@pytest.mark.parametrize("flyby_id_value, flyby_observation_output",
						[("T65", "0211"),
						("T13", "0082"),
						("Ta", "0035"),
						("T57", "0199")])
def testConvertFlybyIDToObservationNumber(flyby_id_value, flyby_observation_output):
	assert pydar.convertFlybyIDToObservationNumber(flyby_id=flyby_id_value) == flyby_observation_output

@pytest.mark.parametrize("flyby_observation_num_value, flyby_id_output",
						[("0211", "T65"),
						("0082", "T13"),
						("0035", "Ta"),
						("0199", "T57")])
def testconvertObservationNumberToFlybyID(flyby_observation_num_value, flyby_id_output):
	assert pydar.convertObservationNumberToFlybyID(flyby_observation_num=flyby_observation_num_value) == flyby_id_output

### extractFlybyDataImages() Function Call
invalid_types = [(1961, "<class 'int'>"),
				(3.1415, "<class 'float'>"),
				([], "<class 'list'>"),
				(False, "<class 'bool'>")]

def testEmptyExtractFlybyDataImages(caplog):
	# Test: Error thrown when extractFlybyDataImages() given no arguments
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages()
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	critical_message = log_record.message.split("\n")[1]
	assert critical_message == "CRITICAL ERROR: Requires either a flyby_observation_num OR flyby_id."
	available_observation_num_message = log_record.message.split("\n")[2]
	assert available_observation_num_message == "Available flyby_observation_num: ['Ta', 'T3', 'T4', 'T7', 'T8', 'T13', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23', 'T25', 'T28', 'T29', 'T30', 'T36', 'T39', 'T41', 'T43', 'T44', 'T48', 'T49', 'T50', 'T52', 'T53', 'T55', 'T56', 'T57', 'T58', 'T59', 'T61', 'T63', 'T64', 'T65', 'T69', 'T71', 'T77', 'T80', 'T83', 'T84', 'T86', 'T91', 'T92', 'T95', 'T98', 'T104']"
	available_id_types_message = log_record.message.split("\n")[3]
	assert available_id_types_message == "Available flyby_id: ['0035', '0045', '0048', '0059', '0065', '0082', '0086', '0087', '0093', '0098', '0100', '0101', '0108', '0111', '0120', '0126', '0127', '0131', '0149', '0157', '0161', '0166', '0167', '0174', '0177', '0181', '0186', '0189', '0193', '0195', '0199', '0200', '0201', '0203', '0209', '0210', '0211', '0218', '0220', '0229', '0234', '0239', '0240', '0243', '0248', '0250', '0253', '0257', '0261']"

def testBothFlybyTypesExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() given both flyby_observation_num and flyby_id
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="0211",
									flyby_id="T31")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR: Requires either a flyby_observation_num OR flyby_id, not both."

@pytest.mark.parametrize("flyby_id_invalid, flyby_error_output", invalid_types)
def testFlybyIDInvalidTypesExtractFlybyDataImage(caplog, flyby_id_invalid, flyby_error_output):
	# Test: Error thrown when extractFlybyDataImages() given invalid flyby_id type values
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_id=flyby_id_invalid, segment_num="S01")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flyby_id]: Must be a str, current type = '{0}'".format(flyby_error_output)

def testNotAvailableFlybyIDNotAvailableExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() given a valid flyby_id that is not in available list
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_id="T32", segment_num="S01")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flyby_id]: 'T32' not in available ids options '['Ta', 'T3', 'T4', 'T7', 'T8', 'T13', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23', 'T25', 'T28', 'T29', 'T30', 'T36', 'T39', 'T41', 'T43', 'T44', 'T48', 'T49', 'T50', 'T52', 'T53', 'T55', 'T56', 'T57', 'T58', 'T59', 'T61', 'T63', 'T64', 'T65', 'T69', 'T71', 'T77', 'T80', 'T83', 'T84', 'T86', 'T91', 'T92', 'T95', 'T98', 'T104']'"

@pytest.mark.parametrize("flyby_observation_num_invalid, flyby_error_output", invalid_types)
def testFlybyObservationNumInvalidTypesExtractFlybyDataImage(caplog, flyby_observation_num_invalid, flyby_error_output):
	# Test: Error thrown when extractFlybyDataImages() given invalid flyby_observation_num type values
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num=flyby_observation_num_invalid, segment_num="S01")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flyby_observation_num]: Must be a str, current type = '{0}'".format(flyby_error_output)

def testNotAvailableFlybyObservationNumNotAvailableExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() given a valid flyby_observation_num that is not in available list
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="1234", segment_num="S01")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flyby_observation_num]: '1234' not in available observation options '['0035', '0045', '0048', '0059', '0065', '0082', '0086', '0087', '0093', '0098', '0100', '0101', '0108', '0111', '0120', '0126', '0127', '0131', '0149', '0157', '0161', '0166', '0167', '0174', '0177', '0181', '0186', '0189', '0193', '0195', '0199', '0200', '0201', '0203', '0209', '0210', '0211', '0218', '0220', '0229', '0234', '0239', '0240', '0243', '0248', '0250', '0253', '0257', '0261']'"

def testSegmentNumRequiredExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() requires a segment_num (is not None)
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [segment_num]: segment_num number required out of available options ['S01', 'S02', 'S03', 'S04'], none given"

@pytest.mark.parametrize("segment_num_invalid, segment_error_output", invalid_types)
def testSegmentNumInvalidTypesExtractFlybyDataImage(caplog, segment_num_invalid, segment_error_output):
	# Test: Error thrown when extractFlybyDataImages() given invalid segment_num type values
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num=segment_num_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [segment_num]: Must be a str, current type = '{0}'".format(segment_error_output)

def testNotAvailableSegmentNumExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() requires a segment_num (is not None)
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num="S05")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [segment_num]: 'S05' not an available segment option '['S01', 'S02', 'S03', 'S04']'"

@pytest.mark.parametrize("resolution_invalid, resolution_error_output", invalid_types)
def testResolutionInvalidTypesExtractFlybyDataImage(caplog, resolution_invalid, resolution_error_output):
	# Test: Error thrown when extractFlybyDataImages() is given invalid resolution types
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num="S01", resolution=resolution_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [resolution]: Must be a str, current type = '{0}'".format(resolution_error_output)

def testNotAvailableResolutionExtractFlybyDataImage(caplog):
	# Test: Error thrown when extractFlybyDataImages() is given a resolution that is not available
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num="S01", resolution="INVALID")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [resolution]: resolution 'INVALID' must be a valid resolution type in {0}".format(pydar.resolution_types)

@pytest.mark.parametrize("top_resolution_invalid, top_resolution_error_output",
						[("1961", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")])
def testTopResolutionInvalidTypesExtractFlybyDataImage(caplog, top_resolution_invalid, top_resolution_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num="S01", top_x_resolutions=top_resolution_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [top_x_resolutions]: Must be a int, current type = '{0}'".format(top_resolution_error_output)

@pytest.mark.parametrize("top_resolution_invalid_range", [(-1), (10)])
def testTopResolutionInvalidTypesExtractFlybyDataImage(caplog, top_resolution_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.extractFlybyDataImages(flyby_observation_num="211", segment_num="S01", top_x_resolutions=top_resolution_invalid_range)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [top_x_resolutions]: Must be a value from 1 to 5, not '{0}'".format(top_resolution_invalid_range)
