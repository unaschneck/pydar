# Pytest for extract_flyby_parameters.py
# pytest -vs --disable-pytest-warnings --show-capture=no
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

'''
def testExtractFlybyDataImages(caplog):
	caplog.clear()
	with caplog.at_level(logging.CRITICAL):
		with pytest.raises(SystemExit) as cm:
			pydar.extractFlybyDataImages()
		assert "CRITICAL ERROR: Requires either a flyby_observation_num OR flyby_id." in caplog.text
	caplog.clear()

def testTesting():
	with pytest.raises(ValueError) as exc_info:
		pydar.testing()
	assert str(exc_info.value) == "hello Titan"
'''
