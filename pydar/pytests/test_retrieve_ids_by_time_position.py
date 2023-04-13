# Pytest for retrieve_ids_by_time_position.py
# pydar/pydar/: pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys -vv
import logging

# External Python libraries (installed via pip install)
import pytest

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

def testFeatureNameRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByFeatureName(feature_name=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [feature_name]: feature_name is required"

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

@pytest.mark.parametrize("feature_name_invalid, feature_error_output", invalid_non_str_options)
def testFeatureNameInvalidTypesRetrieveIDs(caplog, feature_name_invalid, feature_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByFeatureName(feature_name=feature_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [feature_name]: Must be a str, current type = '{0}'".format(feature_error_output)

def testFeatureNameNotValidRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByFeatureName(feature_name="Invalid/Unknown Feature Name")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "Feature Name 'Invalid/Unknown Feature Name' not in available in features list = ['Aaru', 'Abaya Lacus', 'Adiri', 'Afekan', 'Akmena Lacus', 'Albano Lacus', 'Anbus Labyrinthus', 'Angmar Montes', 'Annecy Lacus', 'Antilia Faculae', 'Apanohuaya Flumen', 'Ara Fluctus', 'Arala Lacus', 'Arnar Sinus', 'Arrakis Planitia', 'Arwen Colles', 'Atacama Lacuna', 'Atitlán Lacus', 'Aura Undae', 'Avacha Sinus', 'Aztlan', 'Bacab Virgae', 'Baffin Sinus', 'Balaton Lacus', 'Bayta Fretum', 'Bazaruto Facula', 'Beag', 'Belet', 'Bermoothes Insula', 'Bilbo Colles', 'Bimini Insula', 'Bolsena Lacus', 'Boni Sinus', 'Boreas Undae', 'Bralgu Insulae', 'Brienz Lacus', 'Buada Lacus', 'Buyan Insula', 'Buzzell Planitia', 'Caladan Planitia', 'Cardiel Lacus', 'Cayuga Lacus', 'Celadon Flumina', 'Cerknica Lacuna', 'Chilwa Lacus', 'Ching-tu', 'Chusuk Planitia', 'Coats Facula', 'Concordia Regio', 'Corrin Labyrinthus', 'Crete Facula', 'Crveno Lacus', 'Dilmun', 'Dilolo Lacus', 'Dingle Sinus', 'Dolmed Montes', 'Doom Mons', 'Dridzis Lacus', 'Ecaz Labyrinthus', 'Echoriath Montes', 'Eir Macula', 'Elba Facula', 'Elivagar Flumina', 'Elpis Macula', 'Enriquillo Lacus', 'Erebor Mons', 'Eurus Undae', 'Eyre Lacuna', 'Fagaloa Sinus', 'Faramir Colles', 'Feia Lacus', 'Fensal', 'Flensborg Sinus', 'Fogo Lacus', 'Forseti', 'Freeman Lacus', 'Fundy Sinus', 'Gabes Sinus', 'Gammu Labyrinthus', 'Gamont Labyrinthus', 'Gandalf Colles', 'Ganesa Macula', 'Gansireed Labyrinthus', 'Garotman Terra', 'Gatun Lacus', 'Genetaska Macula', 'Genova Sinus', 'Giedi Planitia', 'Gihon Flumen', 'Ginaz Labyrinthus', 'Gram Montes', 'Grasmere Lacus', 'Grumman Labyrinthus', 'Guabonito', 'Hagal Planitia', 'Hammar Lacus', 'Handir Colles', 'Hano', 'Hardin Fretum', 'Harmonthep Labyrinthus', 'Hawaiki Insulae', 'Hetpet Regio', 'Hlawga Lacus', 'Hobal Virga', 'Hotei Arcus', 'Hotei Regio', 'Hubur Flumen', 'Hufaidh Insulae', 'Huygens Landing Site', 'Ihotry Lacus', 'Imogene Lacus', 'Ipyr Labyrinthus', 'Irensaga Montes', 'Jerid Lacuna', 'Jingpo Lacus', 'Junction Labyrinthus', 'Junín Lacus', 'Kaitain Labyrinthus', 'Kalseru Virga', 'Karakul Lacus', 'Karesos Flumen', 'Kayangan Lacus', 'Kerguelen Facula', 'Kivu Lacus', 'Koitere Lacus', 'Kokytos Flumina', 'Kraken Mare', 'Krocylea Insulae', 'Kronin Labyrinthus', 'Ksa', 'Kumbaru Sinus', 'Kutch Lacuna', 'Ladoga Lacus', 'Lagdo Lacus', 'Lampadas Labyrinthus', 'Lanao Lacus', 'Lankiveil Labyrinthus', 'Leilah Fluctus', 'Lernaeus Labyrinthus', 'Letas Lacus', 'Ligeia Mare', 'Lithui Montes', 'Logtak Lacus', 'Luin Montes', 'Lulworth Sinus', 'Mackay Lacus', 'Maizuru Sinus', 'Manza Sinus', 'Maracaibo Lacus', 'Mayda Insula', 'Melrhir Lacuna', 'Menrva', 'Merlock Montes', 'Meropis Insula', 'Mezzoramia', 'Mindanao Facula', 'Mindolluin Montes', 'Misty Montes', 'Mithrim Montes', 'Mohini Fluctus', 'Momoy', 'Montego Sinus', 'Moray Sinus', 'Moria Montes', 'Muritan Labyrinthus', 'Muzhwi Lacus', 'Mweru Lacus', 'Mystis', 'Müggel Lacus', 'Mývatn Lacus', 'Nakuru Lacuna', 'Naraj Labyrinthus', 'Nath', 'Neagh Lacus', 'Negra Lacus', 'Ngami Lacuna', 'Nicobar Faculae', 'Nicoya Sinus', 'Nimloth Colles', 'Niushe Labyrinthus', 'Notus Undae', 'Oahu Facula', 'Ochumare Regio', 'Ohrid Lacus', 'Okahu Sinus', 'Olomega Lacus', 'Omacatl Macula', 'Oneida Lacus', 'Onogoro Insula', 'Ontario Lacus', 'Orog Lacuna', 'Palma Labyrinthus', 'Patos Sinus', 'Paxsi', 'Penglai Insula', 'Perkunas Virgae', 'Phewa Lacus', 'Pielinen Lacus', 'Planctae Insulae', 'Polaznik Macula', 'Polelya Macula', 'Poritrin Planitia', 'Prespa Lacus', 'Puget Sinus', 'Punga Mare', 'Qinghai Lacus', 'Quilotoa Lacus', 'Quivira', 'Racetrack Lacuna', 'Rannoch Lacus', 'Rerir Montes', 'Richese Labyrinthus', 'Roca Lacus', 'Rohe Fluctus', 'Rombaken Sinus', 'Romo Planitia', 'Rossak Planitia', 'Royllo Insula', 'Rukwa Lacus', 'Rwegura Lacus', 'Saldanha Sinus', 'Salusa Labyrinthus', 'Sambation Flumina', 'Santorini Facula', 'Saraswati Flumen', 'Sarygamysh Lacus', 'Seldon Fretum', 'Selk', 'Senkyo', 'Sevan Lacus', 'Shangri-La', 'Shikoku Facula', 'Shiwanni Virgae', 'Shoji Lacus', 'Sikun Labyrinthus', 'Sinlap', 'Sionascaig Lacus', 'Skelton Sinus', 'Soi', 'Sotonera Lacus', 'Sotra Patera', 'Sparrow Lacus', 'Suwa Lacus', 'Synevyr Lacus', 'Taniquetil Montes', 'Tasmania Facula', 'Taupo Lacus', 'Tengiz Lacus', 'Texel Facula', 'Tishtrya Virgae', 'Tlaloc Virgae', 'Tleilax Labyrinthus', 'Toba Lacus', 'Tollan Terra', 'Tortola Facula', 'Totak Lacus', 'Towada Lacus', 'Trevize Fretum', 'Trichonida Lacus', 'Trold Sinus', 'Tsegihi', 'Tsiipiya Terra', 'Tsomgo Lacus', 'Tui Regio', 'Tumaco Sinus', 'Tunu Sinus', 'Tupile Labyrinthus', 'Uanui Virgae', 'Urmia Lacus', 'Uvs Lacus', 'Uyuni Lacuna', 'Van Lacus', 'Veles', 'Veliko Lacuna', 'Vid Flumina', 'Viedma Lacus', 'Vis Facula', 'Vänern Lacus', 'Waikare Lacus', 'Wakasa Sinus', 'Walvis Sinus', 'Weija Lacus', 'Winia Fluctus', 'Winnipeg Lacus', 'Woytchugga Lacuna', 'Xanadu', 'Xanthus Flumen', 'Xolotlán Lacus', 'Xuttah Planitia', 'Yalaing Terra', 'Yessey Lacus', 'Yojoa Lacus', 'Ypoa Lacus', 'Zaza Lacus', 'Zephyrus Undae', 'Zub Lacus']"

def testLatitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=None, longitude=182)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [latitude]: latitude is required"

def testLongitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [longitude]: longitude is required"

invalid_non_num_options = [("1961", "<class 'str'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

@pytest.mark.parametrize("latitude_invalid, latitude_error_output", invalid_non_num_options)
def testLatitudeInvalidTypesRetrieveIDs(caplog, latitude_invalid, latitude_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=latitude_invalid, longitude=182)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [latitude]: Must be a float or int, current type = '{0}'".format(latitude_error_output)

@pytest.mark.parametrize("longitude_invalid, longitude_error_output", invalid_non_num_options)
def testLongitudeInvalidTypesRetrieveIDs(caplog, longitude_invalid, longitude_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=longitude_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [longitude]: Must be a float or int, current type = '{0}'".format(longitude_error_output)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def testLatitudeInvalidRangeRetrieveIDs(caplog, latitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=latitude_invalid_range, longitude=182)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(latitude_invalid_range)

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def testLatitudeInvalidRangeRetrieveIDs(caplog, longitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitude(latitude=-72, longitude=longitude_invalid_range)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(longitude_invalid_range)

def testMinLatitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=None,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_latitude]: min_latitude is required"

def testMaxLatitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=None,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_latitude]: max_latitude is required"

def testMinLongitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=None,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_longitude]: min_longitude is required"

def testMaxLongitudeRequiredRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_longitude]: max_longitude is required"

invalid_non_num_options = [("1961", "<class 'str'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

@pytest.mark.parametrize("type_invalid, type_error_output", invalid_non_num_options)
def testMinLatitudeInvalidTypesRetrieveIDs(caplog, type_invalid, type_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=type_invalid,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_latitude]: Must be a float or int, current type = '{0}'".format(type_error_output)

@pytest.mark.parametrize("type_invalid, type_error_output", invalid_non_num_options)
def testMaxLatitudeInvalidTypesRetrieveIDs(caplog, type_invalid, type_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=type_invalid,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_latitude]: Must be a float or int, current type = '{0}'".format(type_error_output)

@pytest.mark.parametrize("type_invalid, type_error_output", invalid_non_num_options)
def testMinLongitudeInvalidTypesRetrieveIDs(caplog, type_invalid, type_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=type_invalid,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_longitude]: Must be a float or int, current type = '{0}'".format(type_error_output)

@pytest.mark.parametrize("type_invalid, type_error_output", invalid_non_num_options)
def testMaxLongitudeInvalidTypesRetrieveIDs(caplog, type_invalid, type_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=type_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_longitude]: Must be a float or int, current type = '{0}'".format(type_error_output)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def testMinLatitudeInvalidRangeRetrieveIDs(caplog, latitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=latitude_invalid_range,
												max_latitude=90,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(latitude_invalid_range)

@pytest.mark.parametrize("latitude_invalid_range", [(-91), (91)])
def testMaxLatitudeInvalidRangeRetrieveIDs(caplog, latitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=latitude_invalid_range,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_latitude]: Latitude must be between 90 and -90, current value = '{0}'".format(latitude_invalid_range)

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def testMinLongtiudeInvalidRangeRetrieveIDs(caplog, longitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=longitude_invalid_range,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [min_longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(longitude_invalid_range)

@pytest.mark.parametrize("longitude_invalid_range", [(-1), (361)])
def testMaxLongtiudeInvalidRangeRetrieveIDs(caplog, longitude_invalid_range):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=longitude_invalid_range)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [max_longitude]: Longitude must be between 0 and 360, current value = '{0}'".format(longitude_invalid_range)

def testLatitudeMaxGreaterMinRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=70,
												min_longitude=10,
												max_longitude=20)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [latitude]: max_latitude must be greater than min_latitude"

def testLongitudeMaxGreaterMinRetrieveIDs(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.retrieveIDSByLatitudeLongitudeRange(min_latitude=80,
												max_latitude=90,
												min_longitude=10,
												max_longitude=0)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [longitude]: max_longitude must be greater than min_longtiude"
