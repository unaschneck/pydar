# Pytest for extract_flyby_parameters.py
# pytest -vs --disable-pytest-warnings

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
