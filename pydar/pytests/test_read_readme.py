# Pytest for read_readme.py
# pydar/pydar/: pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys -vv
import logging
import re

# External Python libraries (installed via pip install)
import pytest

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("Testing", "<class 'str'>")]

## returnAAREADMEOptions() #############################################
def test_returnAAREADMEOptions_verifyOptionsOutput(caplog):
	pydar.returnAAREADMEOptions()
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "Line-By-Line Options: ['PDS_VERSION_ID', 'RECORD_TYPE', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_NAME', 'PUBLICATION_DATE', 'NOTE', 'Volume']"
	log_record = caplog.records[1]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "Section Header Options: ['Introduction', 'Disk Format', 'File Formats', 'Volume Contents', 'Recommended DVD Drives and Driver Software', 'Errata and Disclaimer', 'Version Status', 'Contact Information']"
## returnAAREADMEOptions() #############################################

## returnLBLOptions() ##################################################
def test_returnLBLOptions_verifyOptionsOutput(caplog):
	pydar.returnLBLOptions()
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "Line-By-Line Options: ['PDS_VERSION_ID', 'DATA_SET_ID', 'DATA_SET_NAME', 'PRODUCER_INSTITUTION_NAME', 'PRODUCER_ID', 'PRODUCER_FULL_NAME', 'PRODUCT_ID', 'PRODUCT_VERSION_ID', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_HOST_ID', 'INSTRUMENT_NAME', 'INSTRUMENT_ID', 'TARGET_NAME', 'START_TIME', 'STOP_TIME', 'SPACECRAFT_CLOCK_START_COUNT', 'SPACECRAFT_CLOCK_STOP_COUNT', 'PRODUCT_CREATION_TIME', 'SOURCE_PRODUCT_ID', 'MISSION_PHASE_NAME', 'MISSION_NAME', 'SOFTWARE_VERSION_ID', 'FILE_NAME COMPRESSED', 'RECORD_TYPE COMPRESSED', 'ENCODING_TYPE', 'INTERCHANGE_FORMAT', 'UNCOMPRESSED_FILE_NAME', 'REQUIRED_STORAGE_BYTES', '^DESCRIPTION', 'FILE_NAME UNCOMPRESSED', 'RECORD_TYPE UNCOMPRESSED', 'RECORD_BYTES', 'FILE_RECORDS', 'LABEL_RECORDS', '^IMAGE', 'LINES', 'LINE_SAMPLES', 'SAMPLE_TYPE', 'SAMPLE_BITS', 'CHECKSUM', 'SCALING_FACTOR', 'OFFSET', 'MISSING_CONSTANT', 'NOTE', '^DATA_SET_MAP_PROJECTION', 'MAP_PROJECTION_TYPE', 'FIRST_STANDARD_PARALLEL', 'SECOND_STANDARD_PARALLEL', 'A_AXIS_RADIUS', 'B_AXIS_RADIUS', 'C_AXIS_RADIUS', 'POSITIVE_LONGITUDE_DIRECTION', 'CENTER_LATITUDE', 'CENTER_LONGITUDE', 'REFERENCE_LATITUDE', 'REFERENCE_LONGITUDE', 'LINE_FIRST_PIXEL', 'LINE_LAST_PIXEL', 'SAMPLE_FIRST_PIXEL', 'SAMPLE_LAST_PIXEL', 'MAP_PROJECTION_ROTATION', 'MAP_RESOLUTION', 'MAP_SCALE', 'MAXIMUM_LATITUDE', 'MINIMUM_LATITUDE', 'EASTERNMOST_LONGITUDE', 'WESTERNMOST_LONGITUDE', 'LINE_PROJECTION_OFFSET', 'SAMPLE_PROJECTION_OFFSET', 'OBLIQUE_PROJ_POLE_LATITUDE', 'OBLIQUE_PROJ_POLE_LONGITUDE', 'OBLIQUE_PROJ_POLE_ROTATION', 'OBLIQUE_PROJ_X_AXIS_VECTOR', 'OBLIQUE_PROJ_Y_AXIS_VECTOR', 'OBLIQUE_PROJ_Z_AXIS_VECTOR', 'LOOK_DIRECTION', 'COORDINATE_SYSTEM_NAME', 'COORDINATE_SYSTEM_TYPE']"
	log_record = caplog.records[1]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "Section Header Options: ['PRODUCT DESCRIPTION', 'DESCRIPTION OF COMPRESSED AND UNCOMPRESSED FILES', 'POINTERS TO START RECORDS OF OBJECTS IN FILE', 'DESCRIPTION OF OBJECTS CONTAINED IN FILE']"
## returnLBLOptions() ##################################################

## readAAREADME() ######################################################
def test_readAAREADME_coradrRequired():
	with pytest.raises(ValueError, match=re.escape("[coradr_results_directory]: coradr_results_directory is required")):
		pydar.readAAREADME(coradr_results_directory=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_readAAREADME_coradrInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[coradr_results_directory]: Must be a str, current type = '{error_output}'")):
		pydar.readAAREADME(coradr_results_directory=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_readAAREADME_SectionInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[section_to_print]: Must be a str, current type = '{error_output}'")):
		pydar.readAAREADME(coradr_results_directory="coradr_directory", section_to_print=invalid_input)

def test_readAAREADME_NotValidSection():
	with pytest.raises(ValueError, match=re.escape("[readAAREADME]: Cannot find a revelant section_to_print: Invalid 'Invalid Section'")):
		pydar.readAAREADME(coradr_results_directory="coradr_directory", section_to_print="invalid section")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_readAAREADME_PrintInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[print_to_console]: Must be a bool, current type = '{error_output}'")):
		pydar.readAAREADME(coradr_results_directory="coradr_directory", print_to_console=invalid_input)

## readAAREADME() ######################################################

## readLBLREADME() #####################################################
def test_readLBLREADME_coradrRequired():
	with pytest.raises(ValueError, match=re.escape("[coradr_results_directory]: coradr_results_directory is required")):
		pydar.readLBLREADME(coradr_results_directory=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_readLBLREADME_coradrInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[coradr_results_directory]: Must be a str, current type = '{error_output}'")):
		pydar.readLBLREADME(coradr_results_directory=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_readLBLREADME_SectionInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[section_to_print]: Must be a str, current type = '{error_output}'")):
		pydar.readLBLREADME(coradr_results_directory="coradr_directory", section_to_print=invalid_input)

def test_readLBLREADME_NotValidSection():
	with pytest.raises(ValueError, match=re.escape("[readLBLREADME]: Cannot find a revelant section_to_print: Invalid 'INVALID SECTION'")):
		pydar.readLBLREADME(coradr_results_directory="coradr_directory", section_to_print="invalid section")

@pytest.mark.parametrize("unspecific_section", [("FILE_NAME"), ("RECORD_TYPE")])
def test_readLBLREADME_UnspecificSection(unspecific_section):
	with pytest.raises(ValueError, match=re.escape(f"Specify {unspecific_section} as either '{unspecific_section} UNCOMPRESSED' or '{unspecific_section} COMPRESSED'")):
		pydar.readLBLREADME(coradr_results_directory="coradr_directory", section_to_print=unspecific_section)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_readLBLREADME_PrintInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[print_to_console]: Must be a bool, current type = '{error_output}'")):
		pydar.readLBLREADME(coradr_results_directory="coradr_directory", print_to_console=invalid_input)

## readLBLREADME() #####################################################
