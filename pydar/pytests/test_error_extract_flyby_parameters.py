# Test Expected Error Messages from extract_flyby_parameters.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_error_extract_flyby_parameters.py

# Standard Library Imports
import re

# Related Third Party Imports
import pytest

# Internal Local Imports
import pydar

invalid_non_str_options = [(1961, "<class 'int'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]


## id_to_observation() #################################
@pytest.mark.parametrize("flyby_id_value, flyby_observation_output",
                         [("T65", "0211"), ("T13", "0082"), ("Ta", "0035"),
                          ("T57", "0199")])
def test_idToObservation_verifyFlybyConversion(flyby_id_value,
                                               flyby_observation_output):
    assert pydar.id_to_observation(
        flyby_id=flyby_id_value) == flyby_observation_output


## id_to_observation() #################################


## observation_to_id() #################################
@pytest.mark.parametrize("flyby_observation_num_value, flyby_id_output",
                         [("0211", "T65"), ("0082", "T13"), ("0035", "Ta"),
                          ("0199", "T57")])
def test_observationToID_verifyObservationNumberConversion(
        flyby_observation_num_value, flyby_id_output):
    assert pydar.observation_to_id(
        flyby_observation_num=flyby_observation_num_value) == flyby_id_output


## observation_to_id() #################################


## extract_flyby_images() ############################################
def test_extractFlybyImages_verifyFlybyIDOrObservationNumberRequired():
    with pytest.raises(
            ValueError,
            match="Requires either a flyby_observation_num OR flyby_id."):
        pydar.extract_flyby_images()
    #log_record = caplog.records[0]
    #available_observation_num_message = log_record.message.split("\n")[2]
    #assert available_observation_num_message == "Available flyby_observation_num: ['Ta', 'T3', 'T4', 'T7', 'T8', 'T13', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23', 'T25', 'T28', 'T29', 'T30', 'T36', 'T39', 'T41', 'T43', 'T44', 'T48', 'T49', 'T50', 'T52', 'T53', 'T55', 'T56', 'T57', 'T58', 'T59', 'T61', 'T63', 'T64', 'T65', 'T69', 'T71', 'T77', 'T80', 'T83', 'T84', 'T86', 'T91', 'T92', 'T95', 'T98', 'T104']"
    #available_id_types_message = log_record.message.split("\n")[3]
    #assert available_id_types_message == "Available flyby_id: ['0035', '0045', '0048', '0059', '0065', '0082', '0086', '0087', '0093', '0098', '0100', '0101', '0108', '0111', '0120', '0126', '0127', '0131', '0149', '0157', '0161', '0166', '0167', '0174', '0177', '0181', '0186', '0189', '0193', '0195', '0199', '0200', '0201', '0203', '0209', '0210', '0211', '0218', '0220', '0229', '0234', '0239', '0240', '0243', '0248', '0250', '0253', '0257', '0261']"


def test_extractFlybyImages_bothFlybyTypesInvalid():
    with pytest.raises(
            ValueError,
            match=
            "Requires either a flyby_observation_num OR flyby_id, not both."):
        pydar.extract_flyby_images(flyby_observation_num="0211",
                                   flyby_id="T31")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_extractFlybyImages_flybyIDInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flyby_id]: Must be a str, current type = '{error_output}'")
    ):
        pydar.extract_flyby_images(flyby_id=invalid_input, segment_num="S01")


def test_extractFlybyImages_notAvailableFlybyID():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[flyby_id]: 'T32' not in available ids options '['Ta', 'T3', 'T4', 'T7', 'T8', 'T13', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23', 'T25', 'T28', 'T29', 'T30', 'T36', 'T39', 'T41', 'T43', 'T44', 'T48', 'T49', 'T50', 'T52', 'T53', 'T55', 'T56', 'T57', 'T58', 'T59', 'T61', 'T63', 'T64', 'T65', 'T69', 'T71', 'T77', 'T80', 'T83', 'T84', 'T86', 'T91', 'T92', 'T95', 'T98', 'T104']'"
            )):
        pydar.extract_flyby_images(flyby_id="T32", segment_num="S01")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_extractFlybyImages_observationNumInvalidTypes(invalid_input,
                                                       error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flyby_observation_num]: Must be a str, current type = '{error_output}'"
            )):
        pydar.extract_flyby_images(flyby_observation_num=invalid_input,
                                   segment_num="S01")


def test_extractFlybyImages_notAvailableObservationNum():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[flyby_observation_num]: '1234' not in available observation options '['0035', '0045', '0048', '0059', '0065', '0082', '0086', '0087', '0093', '0098', '0100', '0101', '0108', '0111', '0120', '0126', '0127', '0131', '0149', '0157', '0161', '0166', '0167', '0174', '0177', '0181', '0186', '0189', '0193', '0195', '0199', '0200', '0201', '0203', '0209', '0210', '0211', '0218', '0220', '0229', '0234', '0239', '0240', '0243', '0248', '0250', '0253', '0257', '0261']'"
            )):
        pydar.extract_flyby_images(flyby_observation_num="1234",
                                   segment_num="S01")


def test_extractFlybyImages_segmentNumRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[segment_num]: segment_num number required out of available options, none given"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_extractFlybyImages_segmentNumInvalidTypes(invalid_input,
                                                   error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[segment_num]: Must be a str, current type = '{error_output}'"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num=invalid_input)


def test_extractFlybyImages_notAvailableSegmentNum():
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[segment_num]: 'S10' not an available segment options: '{pydar._return_segment_options()}'"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num="S10")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_extractFlybyImages_resolutionInvalidTypes(invalid_input,
                                                   error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[resolution]: Must be a str, current type = '{error_output}'"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num="S01",
                                   resolution=invalid_input)


def test_extractFlybyImages_notAvailableResolution():
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[resolution]: resolution 'INVALID' must be a valid resolution type in {pydar.RESOLUTION_TYPES}"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num="S01",
                                   resolution="INVALID")


@pytest.mark.parametrize("invalid_input, error_output",
                         [("1961", "<class 'str'>"),
                          (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                          (False, "<class 'bool'>")])
def test_extractFlybyImages_topResolutionInvalidTypes(invalid_input,
                                                      error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[top_x_resolutions]: Must be a int, current type = '{error_output}'"
            )):
        pydar.extract_flyby_images(flyby_observation_num="211",
                                   segment_num="S01",
                                   top_x_resolutions=invalid_input)


@pytest.mark.parametrize("top_resolution_invalid_range", [(-1), (10)])
def test_extractFlybyImages_topResolutionInvalidRange(
        top_resolution_invalid_range):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[top_x_resolutions]: Must be a value from 1 to 5, not '{top_resolution_invalid_range}'"
            )):
        pydar.extract_flyby_images(
            flyby_observation_num="211",
            segment_num="S01",
            top_x_resolutions=top_resolution_invalid_range)


## extractFlybyImages() ############################################


## id_to_observation() #################################
def test_idToObsrvation_flybyIDRequired():
    with pytest.raises(ValueError,
                       match=re.escape(
                           "[flyby_id]: A valid flyby_id string is required")):
        pydar.id_to_observation(flyby_id=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_idToObservation_flybyIDInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flyby_id]: Must be a str, current type = '{error_output}'")
    ):
        pydar.id_to_observation(flyby_id=invalid_input)


def test_idToObservation_invalidFlybyID():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[flyby_id]: Invalid flyby_id, 'T32', choose from:\n['Ta', 'T3', 'T4', 'T7', 'T8', 'T13', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23', 'T25', 'T28', 'T29', 'T30', 'T36', 'T39', 'T41', 'T43', 'T44', 'T48', 'T49', 'T50', 'T52', 'T53', 'T55', 'T56', 'T57', 'T58', 'T59', 'T61', 'T63', 'T64', 'T65', 'T69', 'T71', 'T77', 'T80', 'T83', 'T84', 'T86', 'T91', 'T92', 'T95', 'T98', 'T104']"
            )):
        pydar.id_to_observation(flyby_id="T32")


## id_to_observation() #################################


## observation_to_id() #################################
def test_observationToID_observationNumRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[flyby_observation_num]: A valid flyby_observation_num string is required"
            )):
        pydar.observation_to_id(flyby_observation_num=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_observationToID_observationNumInvalidTypes(invalid_input,
                                                    error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flyby_observation_num]: Must be a str, current type = '{error_output}'"
            )):
        pydar.observation_to_id(flyby_observation_num=invalid_input)


def test_observationToID_invalidObservationNum():
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flyby_observation_num]: Invalid flyby_observation_num, '1234', choose from:\n['0035', '0045', '0048', '0059', '0065', '0082', '0086', '0087', '0093', '0098', '0100', '0101', '0108', '0111', '0120', '0126', '0127', '0131', '0149', '0157', '0161', '0166', '0167', '0174', '0177', '0181', '0186', '0189', '0193', '0195', '0199', '0200', '0201', '0203', '0209', '0210', '0211', '0218', '0220', '0229', '0234', '0239', '0240', '0243', '0248', '0250', '0253', '0257', '0261']"
            )):
        pydar.observation_to_id(flyby_observation_num="1234")


## observation_to_id() #################################
