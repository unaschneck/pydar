# Pytest for retrieve_ids_by_time_position.pyc
# pydar/pydar/: pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys -vv
import logging
import re

# External Python libraries (installed via pip install)
import pytest

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

invalid_non_num_options = [("1961", "<class 'str'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_int_options = [("1961", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

## retrieveIDSByFeatureName() ##########################################
def test_retrieveIDSByFeatureName_featureNameRequired():
	with pytest.raises(ValueError, match=re.escape("[feature_name]: feature_name is required")):
		pydar.retrieveIDSByFeatureName(feature_name=None)

def test_retrieveIDSByFeatureName_verifyOutput():
	flyby_ids = pydar.retrieveIDSByFeatureName(feature_name="ontario lacus")
	assert flyby_ids == {'T7': ['S01'], 'T36': ['S03'], 'T39': ['S06', 'S05', 'S01', 'S04'], 'T48': ['S04'], 'T49': ['S01'], 'T50': ['S02'], 'T55': ['S01', 'S03'], 'T56': ['S01'], 'T57': ['S01', 'S02'], 'T58': ['S01'], 'T59': ['S01'], 'T65': ['S04', 'S01', 'S05', 'S02', 'S03'], 'T71': ['S01'], 'T95': ['S03'], 'T98': ['S01', 'S04']}

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_retrieveIDSByFeatureName_featureNameInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[feature_name]: Must be a str, current type = '{error_output}'")):
		pydar.retrieveIDSByFeatureName(feature_name=invalid_input)

def test_retrieveIDSByFeatureName_featureNameNotValid():
	with pytest.raises(ValueError, match=re.escape("Feature Name 'Invalid/Unknown Feature Name' not in available in features list = ['Aaru', 'Abaya Lacus', 'Adiri', 'Afekan', 'Akmena Lacus', 'Albano Lacus', 'Anbus Labyrinthus', 'Angmar Montes', 'Annecy Lacus', 'Antilia Faculae', 'Apanohuaya Flumen', 'Ara Fluctus', 'Arala Lacus', 'Arnar Sinus', 'Arrakis Planitia', 'Arwen Colles', 'Atacama Lacuna', 'Atitlán Lacus', 'Aura Undae', 'Avacha Sinus', 'Aztlan', 'Bacab Virgae', 'Baffin Sinus', 'Balaton Lacus', 'Bayta Fretum', 'Bazaruto Facula', 'Beag', 'Belet', 'Bermoothes Insula', 'Bilbo Colles', 'Bimini Insula', 'Bolsena Lacus', 'Boni Sinus', 'Boreas Undae', 'Bralgu Insulae', 'Brienz Lacus', 'Buada Lacus', 'Buyan Insula', 'Buzzell Planitia', 'Caladan Planitia', 'Cardiel Lacus', 'Cayuga Lacus', 'Celadon Flumina', 'Cerknica Lacuna', 'Chilwa Lacus', 'Ching-tu', 'Chusuk Planitia', 'Coats Facula', 'Concordia Regio', 'Corrin Labyrinthus', 'Crete Facula', 'Crveno Lacus', 'Dilmun', 'Dilolo Lacus', 'Dingle Sinus', 'Dolmed Montes', 'Doom Mons', 'Dridzis Lacus', 'Ecaz Labyrinthus', 'Echoriath Montes', 'Eir Macula', 'Elba Facula', 'Elivagar Flumina', 'Elpis Macula', 'Enriquillo Lacus', 'Erebor Mons', 'Eurus Undae', 'Eyre Lacuna', 'Fagaloa Sinus', 'Faramir Colles', 'Feia Lacus', 'Fensal', 'Flensborg Sinus', 'Fogo Lacus', 'Forseti', 'Freeman Lacus', 'Fundy Sinus', 'Gabes Sinus', 'Gammu Labyrinthus', 'Gamont Labyrinthus', 'Gandalf Colles', 'Ganesa Macula', 'Gansireed Labyrinthus', 'Garotman Terra', 'Gatun Lacus', 'Genetaska Macula', 'Genova Sinus', 'Giedi Planitia', 'Gihon Flumen', 'Ginaz Labyrinthus', 'Gram Montes', 'Grasmere Lacus', 'Grumman Labyrinthus', 'Guabonito', 'Hagal Planitia', 'Hammar Lacus', 'Handir Colles', 'Hano', 'Hardin Fretum', 'Harmonthep Labyrinthus', 'Hawaiki Insulae', 'Hetpet Regio', 'Hlawga Lacus', 'Hobal Virga', 'Hotei Arcus', 'Hotei Regio', 'Hubur Flumen', 'Hufaidh Insulae', 'Huygens Landing Site', 'Ihotry Lacus', 'Imogene Lacus', 'Ipyr Labyrinthus', 'Irensaga Montes', 'Jerid Lacuna', 'Jingpo Lacus', 'Junction Labyrinthus', 'Junín Lacus', 'Kaitain Labyrinthus', 'Kalseru Virga', 'Karakul Lacus', 'Karesos Flumen', 'Kayangan Lacus', 'Kerguelen Facula', 'Kivu Lacus', 'Koitere Lacus', 'Kokytos Flumina', 'Kraken Mare', 'Krocylea Insulae', 'Kronin Labyrinthus', 'Ksa', 'Kumbaru Sinus', 'Kutch Lacuna', 'Ladoga Lacus', 'Lagdo Lacus', 'Lampadas Labyrinthus', 'Lanao Lacus', 'Lankiveil Labyrinthus', 'Leilah Fluctus', 'Lernaeus Labyrinthus', 'Letas Lacus', 'Ligeia Mare', 'Lithui Montes', 'Logtak Lacus', 'Luin Montes', 'Lulworth Sinus', 'Mackay Lacus', 'Maizuru Sinus', 'Manza Sinus', 'Maracaibo Lacus', 'Mayda Insula', 'Melrhir Lacuna', 'Menrva', 'Merlock Montes', 'Meropis Insula', 'Mezzoramia', 'Mindanao Facula', 'Mindolluin Montes', 'Misty Montes', 'Mithrim Montes', 'Mohini Fluctus', 'Momoy', 'Montego Sinus', 'Moray Sinus', 'Moria Montes', 'Muritan Labyrinthus', 'Muzhwi Lacus', 'Mweru Lacus', 'Mystis', 'Müggel Lacus', 'Mývatn Lacus', 'Nakuru Lacuna', 'Naraj Labyrinthus', 'Nath', 'Neagh Lacus', 'Negra Lacus', 'Ngami Lacuna', 'Nicobar Faculae', 'Nicoya Sinus', 'Nimloth Colles', 'Niushe Labyrinthus', 'Notus Undae', 'Oahu Facula', 'Ochumare Regio', 'Ohrid Lacus', 'Okahu Sinus', 'Olomega Lacus', 'Omacatl Macula', 'Oneida Lacus', 'Onogoro Insula', 'Ontario Lacus', 'Orog Lacuna', 'Palma Labyrinthus', 'Patos Sinus', 'Paxsi', 'Penglai Insula', 'Perkunas Virgae', 'Phewa Lacus', 'Pielinen Lacus', 'Planctae Insulae', 'Polaznik Macula', 'Polelya Macula', 'Poritrin Planitia', 'Prespa Lacus', 'Puget Sinus', 'Punga Mare', 'Qinghai Lacus', 'Quilotoa Lacus', 'Quivira', 'Racetrack Lacuna', 'Rannoch Lacus', 'Rerir Montes', 'Richese Labyrinthus', 'Roca Lacus', 'Rohe Fluctus', 'Rombaken Sinus', 'Romo Planitia', 'Rossak Planitia', 'Royllo Insula', 'Rukwa Lacus', 'Rwegura Lacus', 'Saldanha Sinus', 'Salusa Labyrinthus', 'Sambation Flumina', 'Santorini Facula', 'Saraswati Flumen', 'Sarygamysh Lacus', 'Seldon Fretum', 'Selk', 'Senkyo', 'Sevan Lacus', 'Shangri-La', 'Shikoku Facula', 'Shiwanni Virgae', 'Shoji Lacus', 'Sikun Labyrinthus', 'Sinlap', 'Sionascaig Lacus', 'Skelton Sinus', 'Soi', 'Sotonera Lacus', 'Sotra Patera', 'Sparrow Lacus', 'Suwa Lacus', 'Synevyr Lacus', 'Taniquetil Montes', 'Tasmania Facula', 'Taupo Lacus', 'Tengiz Lacus', 'Texel Facula', 'Tishtrya Virgae', 'Tlaloc Virgae', 'Tleilax Labyrinthus', 'Toba Lacus', 'Tollan Terra', 'Tortola Facula', 'Totak Lacus', 'Towada Lacus', 'Trevize Fretum', 'Trichonida Lacus', 'Trold Sinus', 'Tsegihi', 'Tsiipiya Terra', 'Tsomgo Lacus', 'Tui Regio', 'Tumaco Sinus', 'Tunu Sinus', 'Tupile Labyrinthus', 'Uanui Virgae', 'Urmia Lacus', 'Uvs Lacus', 'Uyuni Lacuna', 'Van Lacus', 'Veles', 'Veliko Lacuna', 'Vid Flumina', 'Viedma Lacus', 'Vis Facula', 'Vänern Lacus', 'Waikare Lacus', 'Wakasa Sinus', 'Walvis Sinus', 'Weija Lacus', 'Winia Fluctus', 'Winnipeg Lacus', 'Woytchugga Lacuna', 'Xanadu', 'Xanthus Flumen', 'Xolotlán Lacus', 'Xuttah Planitia', 'Yalaing Terra', 'Yessey Lacus', 'Yojoa Lacus', 'Ypoa Lacus', 'Zaza Lacus', 'Zephyrus Undae', 'Zub Lacus']")):
		pydar.retrieveIDSByFeatureName(feature_name="Invalid/Unknown Feature Name")

## retrieveIDSByFeatureName() ##########################################

## retrieveIDSByLatitudeLongitude() ####################################
def test_retrieveIDSByLatitudeLongitude_latitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[latitude]: latitude is required")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=None, longitude=182)

def test_retrieveIDSByLatitudeLongitude_longitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[longitude]: longitude is required")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=None)

def test_retrieveIDSByLatitudeLongitude_verifyOutput():
	flyby_ids = pydar.retrieveIDSByLatitudeLongitude(latitude=-80, longitude=170)
	assert flyby_ids == {'T39': ['S06', 'S05', 'S01'], 'T49': ['S01'], 'T50': ['S02'], 'T55': ['S03'], 'T56': ['S01'], 'T57': ['S01'], 'T58': ['S01'], 'T59': ['S01'], 'T65': ['S01'], 'T95': ['S03'], 'T98': ['S01', 'S04']}

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitude_latitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[latitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=invalid_input, longitude=182)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitude_longitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[longitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=invalid_input)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def test_retrieveIDSByLatitudeLongitude_latitudeInvalidRange(latitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[latitude]: Latitude must be between 90 and -90, current value = '{latitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=latitude_invalid_range, longitude=182)

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def test_retrieveIDSByLatitudeLongitude_longitudeInvalidRange(longitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[longitude]: Longitude must be between 0 and 360, current value = '{longitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=longitude_invalid_range)

def test_retrieveIDSByLatitudeLongitude_latitudeLongitudeNoIDsRetrieved(caplog):
	pydar.retrieveIDSByLatitudeLongitude(latitude=90, longitude=0)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "\n[WARNING]: No IDs found at latitude from 90 to 90 and longitude from 0 to 0\n"

## retrieveIDSByLatitudeLongitude() ####################################

## retrieveIDSByLatitudeLongitudeRange() ###############################

def test_retrieveIDSByLatitudeLongitudeRange_verifyOutput():
	flyby_ids = pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=-82,
															max_latitude=-72,
															min_longitude=183,
															max_longitude=185)
	assert flyby_ids == {'T7': ['S01'], 'T36': ['S03'], 'T39': ['S06', 'S05', 'S01', 'S04'], 'T48': ['S04'], 'T49': ['S01'], 'T50': ['S02'], 'T55': ['S01', 'S03'], 'T56': ['S01'], 'T57': ['S01', 'S02'], 'T58': ['S01'], 'T59': ['S01'], 'T65': ['S04', 'S01', 'S05', 'S02', 'S03'], 'T71': ['S01'], 'T95': ['S03'], 'T98': ['S01', 'S04']}

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitudeRange_minLatitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[min_latitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=invalid_input,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitudeRange_maxLatitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[max_latitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=invalid_input,
												min_longitude=10,
												max_longitude=20)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitudeRange_minLongitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[min_longitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=invalid_input,
												max_longitude=20)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_retrieveIDSByLatitudeLongitudeRange_maxLongitudeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[max_longitude]: Must be a float or int, current type = '{error_output}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=invalid_input)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def test_retrieveIDSByLatitudeLongitudeRange_minLatitudeInvalidRange(latitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[min_latitude]: Latitude must be between 90 and -90, current value = '{latitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=latitude_invalid_range,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def test_retrieveIDSByLatitudeLongitudeRange_maxLatitudeInvalidRange(latitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[max_latitude]: Latitude must be between 90 and -90, current value = '{latitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=latitude_invalid_range,
												min_longitude=10,
												max_longitude=20)

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def test_retrieveIDSByLatitudeLongitudeRange_minLongtiudeInvalidRange(longitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[min_longitude]: Longitude must be between 0 and 360, current value = '{longitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=longitude_invalid_range,
												max_longitude=20) 

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def test_retrieveIDSByLatitudeLongitudeRange_maxLongtiudeInvalidRange(longitude_invalid_range):
	with pytest.raises(ValueError, match=re.escape(f"[max_longitude]: Longitude must be between 0 and 360, current value = '{longitude_invalid_range}'")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=longitude_invalid_range)

def test_retrieveIDSByLatitudeLongitudeRange_latitudeMaxGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[latitude]: max_latitude must be greater than min_latitude")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=70,
												min_longitude=10,
												max_longitude=20)

def test_retrieveIDSByLatitudeLongitudeRange_longitudeMaxGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[longitude]: max_longitude must be greater than min_longtiude")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=0)

def test_retrieveIDSByLatitudeLongitudeRange_latitudeLongitudeRangeNoIDsRetrieved(caplog):
	pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=89.9999999,
												max_latitude=90,
												min_longitude=359,
												max_longitude=360)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "\n[WARNING]: No IDs found at latitude from 89.9999999 to 90 and longitude from 359 to 360\n"

def test_retrieveIDSByLatitudeLongitudeRange_latitudeLongitudeRangeNoFeaturesRetrieved(caplog):
	pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=89.9999999,
												max_latitude=90,
												min_longitude=359,
												max_longitude=360)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "\n[WARNING]: No IDs found at latitude from 89.9999999 to 90 and longitude from 359 to 360\n"

def test_retrieveIDSByLatitudeLongitudeRange_minLatitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[min_latitude]: min_latitude is required")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=None,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)

def test_retrieveIDSByLatitudeLongitudeRange_maxLatitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[max_latitude]: max_latitude is required")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=None,
												min_longitude=10,
												max_longitude=20)

def test_retrieveIDSByLatitudeLongitudeRange_minLongitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[min_longitude]: min_longitude is required")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=None,
												max_longitude=20)

def test_retrieveIDSByLatitudeLongitudeRange_maxLongitudeRequired():
	with pytest.raises(ValueError, match=re.escape("[max_longitude]: max_longitude is required")):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=None)

## retrieveIDSByLatitudeLongitudeRange() ###############################

## retrieveFeaturesFromLatitudeLongitude() #############################

def test_retrieveFeaturesFromLatitudeLongitude_noFeaturesRetrieved(caplog):
	pydar.retrieveFeaturesFromLatitudeLongitude(latitude=90, longitude=360)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.INFO
	assert log_record.message == "\n[WARNING]: No Features found at latitude from 90 to 90 and longitude from 360 to 360\n"

def test_retrieveIDSByLatitudeLongitude_verifyOutput(caplog):
	found_features = pydar.retrieveFeaturesFromLatitudeLongitude(latitude=-72, longitude=183)
	assert found_features == ['Ontario Lacus', 'Rossak Planitia']

## retrieveFeaturesFromLatitudeLongitude() #############################

## retrieveFeaturesFromLatitudeLongitudeRange() ##########################

def test_retrieveFeaturesFromLatitudeLongitudeRange_verifyOutput(caplog):
	found_features = pydar.retrieveFeaturesFromLatitudeLongitudeRange(min_latitude=-82,
																	max_latitude=-72,
																	min_longitude=183,
																	max_longitude=190)
	assert found_features == ['Crveno Lacus', 'Ontario Lacus', 'Romo Planitia', 'Rossak Planitia', 'Saraswati Flumen']

## retrieveFeaturesFromLatitudeLongitudeRange() ##########################

## retrieveIDSByTime() #################################################
def test_retrieveIDSByTime_yearRequired():
	with pytest.raises(ValueError, match=re.escape("[year]: year is required")):
		pydar.retrieveIDSByTime(year=None, doy=301)

def test_retrieveIDSByTime_DOYRequired():
	with pytest.raises(ValueError, match=re.escape("[doy]: doy is required")):
		pydar.retrieveIDSByTime(year=2005, doy=None)

def test_retrieveIDSByTime_verifyOutput(caplog):
	flyby_ids = pydar.retrieveIDSByTime(year=2005, doy=301)
	assert flyby_ids == {'T8': ['S02', 'S03', 'S01']}
	flyby_ids = pydar.retrieveIDSByTime(year=2005, doy=301, hour=3)
	assert flyby_ids == {'T8': ['S03', 'S01']}

@pytest.mark.parametrize("year_invalid_range", [(2003), (2015)])
def test_retrieveIDSByTime_yearInvalidRange(year_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[year]: year must be between 2004-2014")):
		pydar.retrieveIDSByTime(year=year_invalid_range, doy=301)

@pytest.mark.parametrize("doy_invalid_range", [(-1), (366)])
def test_retrieveIDSByTime_DOYInvalidRange(doy_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[doy]: doy must be between 0-365")):
		pydar.retrieveIDSByTime(year=2005, doy=doy_invalid_range)

@pytest.mark.parametrize("hour_invalid_range", [(-1), (24)])
def test_retrieveIDSByTime_hourInvalidRange(hour_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[hour]: hour must be within UTC range between 0 to 23")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=hour_invalid_range)

@pytest.mark.parametrize("minute_invalid_range", [(-1), (60)])
def test_retrieveIDSByTime_minuteInvalidRange(minute_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[minute]: minute must be within range between 0 to 59")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=minute_invalid_range)

@pytest.mark.parametrize("second_invalid_range", [(-1), (60)])
def test_retrieveIDSByTime_secondInvalidRange(second_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[second]: second must be within range between 0 to 59")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=15, second=second_invalid_range)

@pytest.mark.parametrize("millisecond_invalid_range", [(-1), (1000)])
def test_retrieveIDSByTime_milliscondInvalidRange(millisecond_invalid_range):
	with pytest.raises(ValueError, match=re.escape("[millisecond]: second must be a postive value from 0 to 999")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=15, second=20, millisecond=millisecond_invalid_range)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_yearInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[year]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=invalid_input, doy=301)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_DOYInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[doy]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=2005, doy=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_hourInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[hour]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_minuteInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[minute]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_secondInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[second]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=15, second=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_retrieveIDSByTime_millisecondInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[millisecond]: Must be an int, current type = '{error_output}'")):
		pydar.retrieveIDSByTime(year=2005, doy=301, hour=3, minute=15, second=20, millisecond=invalid_input)

## retrieveIDSByTime() #################################################

## retrieveIDSByTimeRange() ############################################
def test_retrieveIDSByTimeRange_yearStartRequired():
	with pytest.raises(ValueError, match=re.escape("[start_year]: start_year is required")):
		pydar.retrieveIDSByTimeRange(start_year=None, end_year=2011, start_doy=1, end_doy=2)

def test_retrieveIDSByTimeRange_yearEndRequired():
	with pytest.raises(ValueError, match=re.escape("[end_year]: end_year is required")):
		pydar.retrieveIDSByTimeRange(start_year=2010, end_year=None, start_doy=1, end_doy=2)

def test_retrieveIDSByTimeRange_DOYStartRequired(caplog):
	with pytest.raises(ValueError, match=re.escape("[start_doy]: start_doy is required")):
		pydar.retrieveIDSByTimeRange(start_year=2010, end_year=2011, start_doy=None, end_doy=2)

def test_retrieveIDSByTimeRange_verifyOutput():
	flyby_ids = pydar.retrieveIDSByTimeRange(start_year=2004,
											start_doy=299,
											start_hour=2,
											start_minute=15,
											start_second=23,
											start_millisecond=987,
											end_year=2005, 
											end_doy=301,
											end_hour=2,
											end_minute=15,
											end_second=23,
											end_millisecond=987)
	assert flyby_ids == {'Ta': ['S01'], 'T3': ['S01'], 'T7': ['S01']}

def test_retrieveIDSByTimeRange_DOYEndRequired():
	with pytest.raises(ValueError, match=re.escape("[end_doy]: end_doy is required")):
		pydar.retrieveIDSByTimeRange(start_year=2010, end_year=2011, start_doy=1, end_doy=None)

def test_retrieveIDSByTimeRange_yearStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[year]: start_year must be less than/equal to end_year")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2010, start_doy=1, end_doy=2)

def test_retrieveIDSByTimeRange_DOYStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[doy]: start_doy must be less than/equal to end_doy")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2011, start_doy=2, end_doy=1)

def test_retrieveIDSByTimeRange_hourStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[hour]: start_hour must be less than/equal to end_hour")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2011, start_doy=1, end_doy=1, start_hour=2, end_hour=1)

def test_retrieveIDSByTimeRange_minuteStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[minute]: start_minute must be less than/equal to end_minute")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2011, start_doy=1, end_doy=1, start_hour=1, end_hour=1,
									start_minute=2, end_minute=1)

def test_retrieveIDSByTimeRange_secondStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[second]: start_second must be less than/equal to end_second")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2011, start_doy=1, end_doy=1, start_hour=1, end_hour=1,
									start_minute=1, end_minute=1, start_second=2, end_second=1)

def test_retrieveIDSByTimeRange_millisecondStartEndGreaterMin():
	with pytest.raises(ValueError, match=re.escape("[millisecond]: start_millisecond must be less than/equal to end_millisecond")):
		pydar.retrieveIDSByTimeRange(start_year=2011, end_year=2011, start_doy=1, end_doy=1, start_hour=1, end_hour=1,
									start_minute=1, end_minute=1, start_second=1, end_second=1, start_millisecond=2, end_millisecond=1)

## retrieveIDSByTimeRange() ############################################
