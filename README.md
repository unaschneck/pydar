# PYDAR
<picture>
  <source srcset="https://raw.githubusercontent.com/unaschneck/pydar/main/assets/pydar_logo.jpg" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/unaschneck/pydar/main/assets/pydar_logo_black_outline.png">
</picture>

![PyPi](https://img.shields.io/pypi/v/pydar)
![license](https://img.shields.io/github/license/unaschneck/pydar)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)
[![update-dynamic-csv-data-files](https://github.com/unaschneck/pydar/actions/workflows/web_scrap_dynamic_csv_files.yml/badge.svg)](https://github.com/unaschneck/pydar/actions/workflows/web_scrap_dynamic_csv_files.yml)

A Python package to access, download, view, and manipulate Cassini RADAR images in one place

* **Find relevant flyby observation numbers/IDs for a feature, range of latitude/longitudes (or specific latitude/longitude), or a time range (or specific time)**
	* retrieveIDSByFeatureName()
	* retrieveIDSByLatitudeLongitude()
	* retrieveIDSByLatitudeLongitudeRange()
	* retrieveIDSByTime()
	* retrieveIDSByTimeRange()
* **Use flyby observation numbers/IDs to retrieve flyby observation data (.FMT, .TAB, .LBL, .IMG) from SBDR and BIDR by default**
	* extractFlybyDataImages()
	* convertFlybyIDToObservationNumber()
	* convertObservationNumberToFlybyID()
* **Access specific observation data AAREADME and .LBL readme information**
	* returnAllAAREADMEOptions()
	* readAAREADME()
	* returnAllLBLOptions()
	* readLBLREADME()
* **Display PDS image retrieved for flyby observation**
	* displayImages()
* **Extract Metadata from .FMT and .TAB files**
	* extractMetadata()

NOTE: This is Beta quality software that is being actively developed, use at your own risk. This project is not supported or endorsed by either JPL or NASA. The code is provided “as is”, use at your own risk.  

## Overview
For information on instrument specifics and acronyms refer to the [Cassini Radar User Guide](https://pds-imaging.jpl.nasa.gov/documentation/Cassini_RADAR_Users_Guide_2nd_Ed_191004_cmp_200421.pdf)

The Cassini Radar data can be found at the [PDS Imaging Node](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/). The directory is organized by [PDS standards](https://pdssbn.astro.umd.edu/howto/understand.shtml). The file format are defined in the [Small Body Node](https://pdssbn.astro.umd.edu/howto/file_types.shtml). The radar echo is stored originally as floating points in LBDR files. The SAR processors turns the LBDR files to BIDR image. The BIDR data is organized as follows:
```
Cassini RADAR Information (CORADR_xxxx_Vxx) where xxxx is the radar data take number and Vxx is the data version number
  |_ AAREADME.txt
    Information about observation xxxx (xxxx > 0035 for Titan flybys)
  |_CALIB/
  |_CATALOG/
    BIDRDS.CAT: Information about the BIDR dataset
  |_DATA/
  | |_BIDR/
  |   |_ BIbcdeefggg_Dhhh_Tiii_Vnn.LBL: header information for observation < -------- MAIN DATA OF INTEREST'S LABEL
  |   |_ BIbcdeefggg_Dhhh_Tiii_Vnn.ZIP: IMG file compressed in zip file    < -------- MAIN DATA OF INTEREST
  |        |         |                           b  = Kind and bit-type of data
  |        |         |                            F = Primary dataset (incidence-
  |        |         |                                angle-corrected sigma0) in
  |        |         |                                32-bit floating-point format
  |        |         |                                (linear scale, not dB)
  |        |         |                            B = Primary dataset in unsigned
  |        |         |                                byte format (dB, normalized
  |        |         |                                to [0, 255])
  |        |         |                            U = Sigma0 without incidence angle
  |        |         |                                correction in 32-bit floating-
  |        |         |                                point format (linear scale,
  |        |         |                                not dB)
  |        |         |                            E = Incidence angle map, 32-bit
  |        |         |                                floating-point values in degrees
  |        |         |                            T = Latitude map, 32-bit floating-
  |        |         |                                point values in degrees
  |        |         |                            N = Longitude map, 32-bit floating-
  |        |         |                                point values in degrees
  |        |         |                            M = Beam mask map, 8-bit unsigned
  |        |         |                                byte values
  |        |         |                            L = Number of looks map, 32-bit
  |        |         |                                integer values
  |        |         |                            D = standard deviations of Synthetic Aperture Radar 
  | 	   |	     |   			      (SAR) normalized backscatter cross-section noise 
  |	   |	     |				      subtracted values w/o incidence angle correction.
  |	   |	     |				      The values are physical scale (not in dB)
  |	   |         |			          S = Synthetic Aperture Radar (SAR) normalized backscatter cross-section values
  |	   |	     |				      physical scale (not in dB) and have not been corrected for incidence-angle effects.
  |	   |	     |				      Biases due to thermal and quantization noise have been removed.
  |        |         |				  X = Noise equivalent sigma-0 values associated with Synthetic Aperture Radar (SAR) 
  |	   |	     |				      normalized backscatter cross-section noise subtracted values w/o incidence angle 
  |	   |	     |				      correction.  The values are physical scale (not in dB)."
  |        |         |                           c  = Map projection
  |        |         |                            Q = Oblique cylindrical
  |        |         |                           d  = Map resolution
  |        |         |                            B =  2 pixels/degree
  |        |         |                            D =  8 pixels/degree
  |        |         |                            F = 32 pixels/degree
  |        |         |                            G = 64 pixels/degree
  |        |         |                            H = 128 pixels/degree
  |        |         |                            I = 256 pixels/degree
  |        |         |                           ee = Absolute value of latitude at
  |        |         |                                center of file, rounded to
  |        |         |                                nearest degree
  |        |         |                           f  = Hemisphere of center of file
  |        |         |                            N = Northern
  |        |         |                            S = Southern
  |        |         |                          ggg = West longitude at center of
  |        |         |                                file, rounded to nearest degree
  |        |         |                          hhh = 3-digit data take ID
  |        |         |                                (observation counter) from which
  |        |         |                                data are included, left-padded
  |        |         |                                with zeroes as needed
  |        |         |                          iii = 3-digit index of Titan flyby
  |        |         |                                from which data are included,
  |        |         |                                left-padded with zeroes as
  |        |         |                                needed.  (Note:  the index
  |        |         |                                for the "Ta" flyby is "00A")
  |_______ |________ | ____________________     nn  = 2-digit version number
  |
  |_DOCUMENT/
  |_ERRATA.txt
  |_EXTRAS/
    |_BIbcdeefggg_Dhhh_Tiii_Vnn.JPG: jpg of IMG files in DATA 
  |_INDEX/
  |_SOFTWARE/
  |_VOLDESC.CAT <--- VERSION INFORMATION LISTED HERE ('VOLUME_VERSION_ID' = "Version 1", "Version 2", "Version 3") and in filename
```

.IMG files can be viewed using the [planetary images library](https://planetaryimage.readthedocs.io/_/downloads/en/latest/pdf/)

### Download Time
Download time varies depending on the number and size of files of interest. On average, most single feature downloads take between 2-10 minutes to download.

![image](https://user-images.githubusercontent.com/24469269/211881026-5bab329c-cf0d-416b-bedc-6d466b77b1f5.png)
([Cassini Radar Volume SIS, Version 2.1](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0284/DOCUMENT/VOLSIS.PDF) Table 1, pg. 3)

### Cross-Reference Table for Observations and Flybys
The Titan flybys ID is not used in the naming convention for the CORADR filenames. The Titan flyby information is contained in the BIDR filenames and in the VOLDESC.CAT under 'Description' and can be found using the following cross-reference table: [cassini_flyby.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/cassini_flyby.csv)

To convert between a Titan Flyby ID and an observation number use either `pydar.convertFlybyIDToObservationNumber(flyby_id)` or `pydar.convertObservationNumberToFlybyID(flyby_observation_num)`

### Observation Information as filename
The data filename contains a lot of information about the observation

(EXAMPLE) Filename: "BIBQD05S184_D065_T008S03_V03"

- BI = BIDR data
- B = data in dB normalized
- Q = obliquid dylindrical
- D = 8 pixels/degree
- 05 = absolute value of latitude at center rounded to nearest degree
- S = hemisphere of center of file (Southern)
- 184 = West longitude at center of file rounded to nearest degree
- D065 = 2-digit data take ID aka observation counter with left-padded zeros
- T008 = 3-digit Titan flyby with left-padding
- S03 = 2-digit segment number (00-99)
- V03 = 2-digit version number (01-99)

Image file from BIBQD05S184_D065_T008S03_V03.JPG:

![BIFQI10S251_D065_T008S01_V03](https://user-images.githubusercontent.com/24469269/210164143-427003ed-0043-45b4-a80f-8e9ddf28543a.jpg)

### Volume Version of Data

Some passes have multiple versions of the data, up to 3 different versions currently.

* Version 1 (V01) was the first archived version of the data and assumed Titan had zero obliquity, which resulted in misregistration between passes

* Version 2 (V02) used a Titan spin model that reduced misregistration error 

* Version 3 (V03) used a long-term, accurate spin model for Titan along with other improvements

Only some Titan passes produced all of the version numbers.

* TA-T25 : V01, V02, V03

* $\gt$ T28: V02, V03

* T108-T126: labeled only once as V02 but is actually V03

The version number is listed in the filename and in VOLDESC.CAT under the 'VOLUME_VERSION_ID'

**Version 3 is the latest and preferred version**

Example:

Version 1 is named BIFQI48N071_D035_T00A_V01.IMG

Version 2 is named BIFQI49N071_D035_T00AS01_V02.IMG

Version 3 is named BIFQI49N071_D035_T00AS01_V03.IMG

### Segment Number of Data
A single flyby can produce multiple image segments (Sxx). *S01 is the primary imaging segment* with other segments referring to periods in the flyby when the instrument went to/from altimetry/SAR/HiSAR or weird pointing profiles.  

![image](https://user-images.githubusercontent.com/24469269/210197286-c059ffed-281d-46c7-911a-f86c3bf7ea28.png)
*Credit: Cassini Radar User Guide (Wall et al. 2019, pg.16)*

## Data Files

### Dynamically Updated Backend Data Files

Pydar includes multiple scripts to web scrap from revelant URLs to generate some of the backend data files

Changes are checked once a month via Github Actions to keep csv files up to date and any changes found will be bundled into the subsequent release

**coradr_jpl_options.csv**

Contains all the CORADR IDs and data types from [pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter)

Columns: ["CORADR ID", "Is a Titan Flyby", "Contains ABDR", "Contains ASUM", "Contains BIDR", "Contains LBDR", "Contains SBDR", "Contains STDR"]

View data file: [coradr_jpl_options.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/coradr_jpl_options.csv)

**swath_coverage_by_time_position.csv**

Contains all the information for .LBL files within a CORADR ID page (for each segment and resolution file) by looking within a specific CORADR IDs /DATA/BIDR for .LBL files

Columns: ["CORADR ID", "FLYBY ID", "SEGMENT NUMBER", "FILENAME", "DATE TYPE SYMBOL", "DATE TYPE", "RESOLUTION (pixels/degrees)", "TARGET_NAME", "MAXIMUM_LATITUDE (Degrees)", "MINIMUM_LATITUDE (Degrees)", "EASTERNMOST_LONGITUDE (Degrees)", "WESTERNMOST_LONGITUDE (Degrees)", "START_TIME", "STOP_TIME"]

View data file: [swath_coverage_by_time_position.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/swath_coverage_by_time_position.csv)

**feature_name_details.csv**

Contains all named features on Titan with names with their associated position and the origin of their name. Taken from the [planetarynames.wr.usgs.gov](https://planetarynames.wr.usgs.gov/SearchResults?Target=74_Titan)

Columns: ["Feature Name", "Northernmost Latitude", "Southernmost Latitude", "Easternmost Longitude", "Westernmost Longitude", "Center Latitude", "Center Longitude", "Origin of Name"]

View data file: [feature_name_details.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/feature_name_details.csv)

### Static Data Files

**cassini_flyby.csv**

Reference for converting between a Titan Flyby ID (e.g. "T7") to an Observation Number (e.g. "059") (and back)

Columns: ["Titan flyby id", "Radar Data Take Number", "Sequence number", "Orbit Number/ID"]

View data file: [cassini_flyby.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/cassini_flyby.csv)

**sar_swath_details.csv**

Currently unused, but will potentially be used in the future for incidence angle, polarization, azimuth, SAR range resolution, SAR azimuth resolution, and number of looks

Converted to a static csv file from the Cassini User Guide (pg. 136-139)

View data file: [sar_swath_details.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/sar_swath_details.csv)

## SBDR Files
Total width of the RADAR swath is created by combining the five individual sub-swaths, where the center beam is the highest gain
![image](https://user-images.githubusercontent.com/24469269/211431884-c201ac74-114a-4c17-b95a-f9edf0178d2e.png)
(_The Cassini Huygens Mission: Orbiter Remote Sensing Observation 2004_)

[SBDR column descriptions](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0045/DOCUMENT/BODPSIS.PDF)

```
test_file = "SBDR_15_D065_V03.TAB"
SBDR_FILE = pdr.read(test_file)
print("Table options: {0}".format(SBDR_FILE.keys()))
```

## BIDR and SBDR Files
Note: "CORADR_0048", "CORADR_0186", "CORADR_0189", "CORADR_0209", "CORADR_0234" do not have associated BIDR values.

There are data gaps and problems from the original downlinking and satellite location

CORADR_0048 (T4) did not have SAR data, only scatterometry and radiometery because of telemetry reasons in the handbook

CORADR_0186 (T52) only have rad and compressed scatterometry

CORADR_189 (T53) only has rad and compressed scatterometry because of what appears to be a downlink problem

CORADR_0209 (T63) only has scatterometry and radiometry

CORADR_0234 (T80) only has scatterometry and radiometry 

## Dependencies
Python 3.7+

Verified compatibility with Python 3.7, 3.8, and 3.9

```
pip3 install -r requirements.txt
```

Requirements will also be downloaded as part of the pip download

## Install
PyPi pip install at [pypi.org/project/pydar/](https://pypi.org/project/pydar/)

```
pip install pydar
```

## Retrieve Data from CASSINI

To collect flyby information and images from a feature on Titan, start by selecting a feature, for example: "Ontario Lacus"

**retrieveIDSByFeatureName**

Retrieve a list of flyby IDs with their associated segments based on a feature name from titan

```python
retrieveIDSByFeatureName(feature_name=None)
```
* **[REQUIRED]** feature_name (string): Feature name on Titan to give flyby ids and segments, not case-sensitive

Feature names are retrieved from [feature_name_details.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/feature_name_details.csv)
<details closed>
<summary>List of Valid Feature Names (Click to view all)</summary>
<br>
['Aaru', 'Abaya Lacus', 'Adiri', 'Afekan', 'Akmena Lacus', 'Albano Lacus', 'Anbus Labyrinthus', 'Angmar Montes', 'Annecy Lacus', 'Antilia Faculae', 'Apanohuaya Flumen', 'Ara Fluctus', 'Arala Lacus', 'Arnar Sinus', 'Arrakis Planitia', 'Arwen Colles', 'Atacama Lacuna', 'Atitlán Lacus', 'Aura Undae', 'Avacha Sinus', 'Aztlan', 'Bacab Virgae', 'Baffin Sinus', 'Balaton Lacus', 'Bayta Fretum', 'Bazaruto Facula', 'Beag', 'Belet', 'Bermoothes Insula', 'Bilbo Colles', 'Bimini Insula', 'Bolsena Lacus', 'Boni Sinus', 'Boreas Undae', 'Bralgu Insulae', 'Brienz Lacus', 'Buada Lacus', 'Buyan Insula', 'Buzzell Planitia', 'Caladan Planitia', 'Cardiel Lacus', 'Cayuga Lacus', 'Celadon Flumina', 'Cerknica Lacuna', 'Chilwa Lacus', 'Ching-tu', 'Chusuk Planitia', 'Coats Facula', 'Concordia Regio', 'Corrin Labyrinthus', 'Crete Facula', 'Crveno Lacus', 'Dilmun', 'Dilolo Lacus', 'Dingle Sinus', 'Dolmed Montes', 'Doom Mons', 'Dridzis Lacus', 'Ecaz Labyrinthus', 'Echoriath Montes', 'Eir Macula', 'Elba Facula', 'Elivagar Flumina', 'Elpis Macula', 'Enriquillo Lacus', 'Erebor Mons', 'Eurus Undae', 'Eyre Lacuna', 'Fagaloa Sinus', 'Faramir Colles', 'Feia Lacus', 'Fensal', 'Flensborg Sinus', 'Fogo Lacus', 'Forseti', 'Freeman Lacus', 'Fundy Sinus', 'Gabes Sinus', 'Gammu Labyrinthus', 'Gamont Labyrinthus', 'Gandalf Colles', 'Ganesa Macula', 'Gansireed Labyrinthus', 'Garotman Terra', 'Gatun Lacus', 'Genetaska Macula', 'Genova Sinus', 'Giedi Planitia', 'Gihon Flumen', 'Ginaz Labyrinthus', 'Gram Montes', 'Grasmere Lacus', 'Grumman Labyrinthus', 'Guabonito', 'Hagal Planitia', 'Hammar Lacus', 'Handir Colles', 'Hano', 'Hardin Fretum', 'Harmonthep Labyrinthus', 'Hawaiki Insulae', 'Hetpet Regio', 'Hlawga Lacus', 'Hobal Virga', 'Hotei Arcus', 'Hotei Regio', 'Hubur Flumen', 'Hufaidh Insulae', 'Huygens Landing Site', 'Ihotry Lacus', 'Imogene Lacus', 'Ipyr Labyrinthus', 'Irensaga Montes', 'Jerid Lacuna', 'Jingpo Lacus', 'Junction Labyrinthus', 'Junín Lacus', 'Kaitain Labyrinthus', 'Kalseru Virga', 'Karakul Lacus', 'Karesos Flumen', 'Kayangan Lacus', 'Kerguelen Facula', 'Kivu Lacus', 'Koitere Lacus', 'Kokytos Flumina', 'Kraken Mare', 'Krocylea Insulae', 'Kronin Labyrinthus', 'Ksa', 'Kumbaru Sinus', 'Kutch Lacuna', 'Ladoga Lacus', 'Lagdo Lacus', 'Lampadas Labyrinthus', 'Lanao Lacus', 'Lankiveil Labyrinthus', 'Leilah Fluctus', 'Lernaeus Labyrinthus', 'Letas Lacus', 'Ligeia Mare', 'Lithui Montes', 'Logtak Lacus', 'Luin Montes', 'Lulworth Sinus', 'Mackay Lacus', 'Maizuru Sinus', 'Manza Sinus', 'Maracaibo Lacus', 'Mayda Insula', 'Melrhir Lacuna', 'Menrva', 'Merlock Montes', 'Meropis Insula', 'Mezzoramia', 'Mindanao Facula', 'Mindolluin Montes', 'Misty Montes', 'Mithrim Montes', 'Mohini Fluctus', 'Momoy', 'Montego Sinus', 'Moray Sinus', 'Moria Montes', 'Muritan Labyrinthus', 'Muzhwi Lacus', 'Mweru Lacus', 'Mystis', 'Müggel Lacus', 'Mývatn Lacus', 'Nakuru Lacuna', 'Naraj Labyrinthus', 'Nath', 'Neagh Lacus', 'Negra Lacus', 'Ngami Lacuna', 'Nicobar Faculae', 'Nicoya Sinus', 'Nimloth Colles', 'Niushe Labyrinthus', 'Notus Undae', 'Oahu Facula', 'Ochumare Regio', 'Ohrid Lacus', 'Okahu Sinus', 'Olomega Lacus', 'Omacatl Macula', 'Oneida Lacus', 'Onogoro Insula', 'Ontario Lacus', 'Orog Lacuna', 'Palma Labyrinthus', 'Patos Sinus', 'Paxsi', 'Penglai Insula', 'Perkunas Virgae', 'Phewa Lacus', 'Pielinen Lacus', 'Planctae Insulae', 'Polaznik Macula', 'Polelya Macula', 'Poritrin Planitia', 'Prespa Lacus', 'Puget Sinus', 'Punga Mare', 'Qinghai Lacus', 'Quilotoa Lacus', 'Quivira', 'Racetrack Lacuna', 'Rannoch Lacus', 'Rerir Montes', 'Richese Labyrinthus', 'Roca Lacus', 'Rohe Fluctus', 'Rombaken Sinus', 'Romo Planitia', 'Rossak Planitia', 'Royllo Insula', 'Rukwa Lacus', 'Rwegura Lacus', 'Saldanha Sinus', 'Salusa Labyrinthus', 'Sambation Flumina', 'Santorini Facula', 'Saraswati Flumen', 'Sarygamysh Lacus', 'Seldon Fretum', 'Selk', 'Senkyo', 'Sevan Lacus', 'Shangri-La', 'Shikoku Facula', 'Shiwanni Virgae', 'Shoji Lacus', 'Sikun Labyrinthus', 'Sinlap', 'Sionascaig Lacus', 'Skelton Sinus', 'Soi', 'Sotonera Lacus', 'Sotra Patera', 'Sparrow Lacus', 'Suwa Lacus', 'Synevyr Lacus', 'Taniquetil Montes', 'Tasmania Facula', 'Taupo Lacus', 'Tengiz Lacus', 'Texel Facula', 'Tishtrya Virgae', 'Tlaloc Virgae', 'Tleilax Labyrinthus', 'Toba Lacus', 'Tollan Terra', 'Tortola Facula', 'Totak Lacus', 'Towada Lacus', 'Trevize Fretum', 'Trichonida Lacus', 'Trold Sinus', 'Tsegihi', 'Tsiipiya Terra', 'Tsomgo Lacus', 'Tui Regio', 'Tumaco Sinus', 'Tunu Sinus', 'Tupile Labyrinthus', 'Uanui Virgae', 'Urmia Lacus', 'Uvs Lacus', 'Uyuni Lacuna', 'Van Lacus', 'Veles', 'Veliko Lacuna', 'Vid Flumina', 'Viedma Lacus', 'Vis Facula', 'Vänern Lacus', 'Waikare Lacus', 'Wakasa Sinus', 'Walvis Sinus', 'Weija Lacus', 'Winia Fluctus', 'Winnipeg Lacus', 'Woytchugga Lacuna', 'Xanadu', 'Xanthus Flumen', 'Xolotlán Lacus', 'Xuttah Planitia', 'Yalaing Terra', 'Yessey Lacus', 'Yojoa Lacus', 'Ypoa Lacus', 'Zaza Lacus', 'Zephyrus Undae', 'Zub Lacus']
</details>

```python
import pydar
pydar.retrieveIDSByFeatureName(feature_name="Ontario Lacus")
```
Output = `{'T7': ['S01'], 'T39': ['S04'], 'T71': ['S01']}`

**retrieveIDSByLatitudeLongitude**

Retrieve a list of flyby IDs with their associated segments based on specific latitude and longitude

```python
retrieveIDSByLatitudeLongitude(latitude=None, longitude=None)
```
* **[REQUIRED]** latitude (float/int): Latitude (in degrees), range from -90° to 90°
* **[REQUIRED]** longitude (float/int): Longitude (in degrees), range from 0° to 360°

```python
import pydar
pydar.retrieveIDSByLatitudeLongitude(latitude=10, longitude=10)
```
Output = `{'T104': ['S01']}`

**retrieveIDSByLatitudeLongitudeRange**

Retrieve a list of flyby IDs with their associated segments based on range of latitudes and longitudes

```python
retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=None,
				southernmost_latitude=None,
				easternmost_longitude=None,
				westernmost_longitude=None)
```
* **[REQUIRED]** northernmost_latitude (float/int): Latitude (in degrees) where North must be greater than or equal to the south, range from -90° to 90°
* **[REQUIRED]** southernmost_latitude (float/int): Latitude (in degrees) where South must be less than or euqal to the north, range from -90° to 90°
* **[REQUIRED]** easternmost_longitude (float/int): Longitude (in degrees) where West must be less than or equal to the east, range from 0° to 360°
* **[REQUIRED]** westernmost_longitude (float/int): Longitude (in degrees) where East be greater than or equal to the west, range from 0° to 360°

```python
retrieveIDSByLatitudeLongitudeRange(southernmost_latitude=19,
				northernmost_latitude=30,
				westernmost_longitude=130,
				easternmost_longitude=140)
```
Output = `{'Ta': ['S01'], 'T3': ['S01'], 'T23': ['S01'], 'T25': ['S01'], 'T28': ['S01'], 'T50': ['S01'], 'T69': ['S02'], 'T84': ['S03', 'S01'], 'T86': ['S01'], 'T104': ['S01', 'S02']}`

Ontario Lacus was visible in four swath observations: T57, T58, T65, T98 [(Page 163)](https://pds-imaging.jpl.nasa.gov/documentation/Cassini_RADAR_Users_Guide_2nd_Ed_191004_cmp_200421.pdf).

To access flyby of Ontario, first specify a flyby. For this example, Ontario Lacus with the features:

* Titan flyby id: 'T65'
* resolution: 'D' (8 pixels/degree)
* Main imaging segement 1: 'S01'

**extractFlybyDataImages()**

Downloads flyby data SBDR: .FMT and .TAB files (for example: [SBDR.FMT](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/SBDR/SBDR.FMT) and [SBDR_15_D087_V03.TAB](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/SBDR/SBDR_15_D087_V03.TAB))

Downloads flyby data BIDR: .LBL and .ZIP files (for example: [BIBQH80N051_D087_T016S01_V03.LBL](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/BIDR/BIBQH80N051_D087_T016S01_V03.LBL) and [BIBQH80N051_D087_T016S01_V03.ZIP](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/BIDR/BIBQH80N051_D087_T016S01_V03.ZIP))

```
extractFlybyDataImages(flyby_observation_num=None,
			flyby_id=None,
			segment_num=None,
			additional_data_types_to_download=[],
			resolution='I',
			top_x_resolutions=None)
```
Either a flyby_id (for example: 'T65') or a flyby_observation_num (for example: '0065') is required. A flyby_id will be translated into a flyby_observation_number to access on the backend and the results will be saved under the observation number. 'T65' will become observation number '0021'

* **[REQUIRED/OPTIONAL]** flyby_observation_num (string): required if flyby_id not included
* **[REQUIRED/OPTIONAL]** flyby_id (string): required if flyby_observation_num not included
* **[REQUIRED]** segment_num (string): a flyby includes multiple image segments (S0X) where S01 is the primary imaging segment ["S01", "S02", "S03"]
* [OPTIONAL] additional_data_types_to_download (List of Strings): Possible options ["ABDR", "ASUM", "BIDR", "LBDR", "SBDR", "STDR"] (__NOTE__: current functionality does not download any additional data types)
* [OPTIONAL] resolution (String): resolution options "B", "D", "F", "H", or "I" (2, 8, 32, 128, 256 pixels/degree), defaults to highest resolution 'I'
* [OPTIONAL] top_x_resolutions: Save the top x resolution types (5 total resolutions)

```python
import pydar
pydar.extractFlybyDataImages(flyby_id='T65',
			resolution='D',
			segment_num="S01",
			additional_data_types_to_download=["STDR", "LBDR"])
```

extractFlybyDataImages() will retrieve images from PDS website and saves results in a directory labeled 'pydar_results' with the flyby obsrevation number, version number, and segement number in the title (for example pydar_results/CORADR_0065_V03_S01)

**convertFlybyIDToObservationNumber**

Converts a Titan Flyby ID (for example: 'T65') to an observation number with front padding ('T65' -> '0211')

```python
convertFlybyIDToObservationNumber(flyby_id)
```
* **[REQUIRED/OPTIONAL]** flyby_id (string): a valid flyby ID with prefix 'T'

```python
import pydar
observation_number = convertFlybyIDToObservationNumber(flyby_id='T65')
```
Output = `0211`

Observation number based on the 'Radar Data Take Number' in the cassini_flyby.csv file with front padding to ensure that all observation numbers are 4 digits long (0065 and 0211)

**convertObservationNumberToFlybyID**

Converts a Titan Observation Number (for example: '211' or '0211') to an flyby id ('0211' -> 'T65')

```python
convertObservationNumberToFlybyID(flyby_observation_num)
```
* **[REQUIRED/OPTIONAL]** flyby_observation_num (string): a valid observation number

```python
import pydar
flyby_id = convertObservationNumberToFlybyID(flyby_observation_num='211')
```
Output = `T65`

Flyby ids are based on the 'Radar Data Take Number' in the cassini_flyby.csv file with front padding of 'T'

Requires each Titan flyby ID to be a valid value the cassini_flyby.csv 

**readAAREADME**

Print AAREADME.TXT to console for viewing

```
readAAREADME(coradr_results_directory=None,
	section_to_print=None, 
	print_to_console=True)
```

* **[REQUIRED]** coradr_results_directory (string):
* [OPTIONAL] section_to_print (string): Specify a section to print to console from the AAREADME, defaults to print the entire AAREADME.TXT, not case-sensitive 
* [OPTIONAL] print_to_console (boolean): Print to console, defaults to true, otherwise function will return output as a string

To see a list of all section_to_print options, see: returnAllAAREADMEOptions()

```python
import pydar
pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0065_V03_S01",
		section_to_print="Volume")
```
Output = "Volume CORADR_0065:  Titan Flyby T8, Sequence S15, Oct 27, 2005"

To get the section that are avaiable for printing: returnAllAAREADMEOptions()

```python
import pydar
pydar.returnAllAAREADMEOptions()
```

Output = `['PDS_VERSION_ID', 'RECORD_TYPE', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_NAME', 'PUBLICATION_DATE', 'NOTE', 'END_OBJECT', 'Volume', 'Introduction', 'Disk Format', 'File Formats', 'Volume Contents', 'Recommended DVD Drives and Driver Software', 'Errata and Disclaimer', 'Version Status', 'Contact Information']`

**readLBLREADME**

Print .LBL README to console for viewing

```
readLBLREADME(coradr_results_directory=None,
	section_to_print=None, 
	print_to_console=True)
```

* **[REQUIRED]** coradr_results_directory (string):
* [OPTIONAL] section_to_print (string): Specify a section to print to console from the AAREADME, defaults to print the entire AAREADME.TXT, not case-sensitive
* [OPTIONAL] print_to_console (boolean): Print to console, defaults to true, otherwise function will return output as a string

To see a list of all section_to_print options, see: returnAllLBLOptions()

```python
import pydar
pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0035_S01/",
		section_to_print="OBLIQUE_PROJ_X_AXIS_VECTOR")
```
Output = `(0.13498322,0.00221225,-0.99084542)`

To get the sections that are available for printing: returnAllLBLOptions()
```python
import pydar
pydar.returnAllLBLOptions()
```
<details closed>
<summary>Line-By-Line Options (Click to view all)</summary>
<br>
['PDS_VERSION_ID', 'DATA_SET_ID', 'DATA_SET_NAME', 'PRODUCER_INSTITUTION_NAME', 'PRODUCER_ID', 'PRODUCER_FULL_NAME', 'PRODUCT_ID', 'PRODUCT_VERSION_ID', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_HOST_ID', 'INSTRUMENT_NAME', 'INSTRUMENT_ID', 'TARGET_NAME', 'START_TIME', 'STOP_TIME', 'SPACECRAFT_CLOCK_START_COUNT', 'SPACECRAFT_CLOCK_STOP_COUNT', 'PRODUCT_CREATION_TIME', 'SOURCE_PRODUCT_ID', 'MISSION_PHASE_NAME', 'MISSION_NAME', 'SOFTWARE_VERSION_ID', 'FILE_NAME COMPRESSED', 'RECORD_TYPE COMPRESSED', 'ENCODING_TYPE', 'INTERCHANGE_FORMAT', 'UNCOMPRESSED_FILE_NAME', 'REQUIRED_STORAGE_BYTES', '^DESCRIPTION', 'FILE_NAME UNCOMPRESSED', 'RECORD_TYPE UNCOMPRESSED', 'RECORD_BYTES', 'FILE_RECORDS', 'LABEL_RECORDS', '^IMAGE', 'LINES', 'LINE_SAMPLES', 'SAMPLE_TYPE', 'SAMPLE_BITS', 'CHECKSUM', 'SCALING_FACTOR', 'OFFSET', 'MISSING_CONSTANT', 'NOTE', '^DATA_SET_MAP_PROJECTION', 'MAP_PROJECTION_TYPE', 'FIRST_STANDARD_PARALLEL', 'SECOND_STANDARD_PARALLEL', 'A_AXIS_RADIUS', 'B_AXIS_RADIUS', 'C_AXIS_RADIUS', 'POSITIVE_LONGITUDE_DIRECTION', 'CENTER_LATITUDE', 'CENTER_LONGITUDE', 'REFERENCE_LATITUDE', 'REFERENCE_LONGITUDE', 'LINE_FIRST_PIXEL', 'LINE_LAST_PIXEL', 'SAMPLE_FIRST_PIXEL', 'SAMPLE_LAST_PIXEL', 'MAP_PROJECTION_ROTATION', 'MAP_RESOLUTION', 'MAP_SCALE', 'MAXIMUM_LATITUDE', 'MINIMUM_LATITUDE', 'EASTERNMOST_LONGITUDE', 'WESTERNMOST_LONGITUDE', 'LINE_PROJECTION_OFFSET', 'SAMPLE_PROJECTION_OFFSET', 'OBLIQUE_PROJ_POLE_LATITUDE', 'OBLIQUE_PROJ_POLE_LONGITUDE', 'OBLIQUE_PROJ_POLE_ROTATION', 'OBLIQUE_PROJ_X_AXIS_VECTOR', 'OBLIQUE_PROJ_Y_AXIS_VECTOR', 'OBLIQUE_PROJ_Z_AXIS_VECTOR', 'LOOK_DIRECTION', 'COORDINATE_SYSTEM_NAME', 'COORDINATE_SYSTEM_TYPE']
</details>
<details closed>
<summary>Section Header Options (Click to view all)</summary>
<br>
['PRODUCT DESCRIPTION', 'DESCRIPTION OF COMPRESSED AND UNCOMPRESSED FILES', 'POINTERS TO START RECORDS OF OBJECTS IN FILE', 'DESCRIPTION OF OBJECTS CONTAINED IN FILE']
</details>

**retrieveFeaturesFromLatitudeLongitude**

Return a list of features found at a specific latitude/longitude position

```
retrieveFeaturesFromLatitudeLongitude(latitude=None, longitude=None)
```
* **[REQUIRED]** latitude (float/int): Latitude (in degrees), range from -90° to 90°
* **[REQUIRED]** longitude (float/int): Longitude (in degrees), range from 0° to 360°

```python
import pydar
pydar.retrieveFeaturesFromLatitudeLongitude(latitude=-72, longitude=183)
```

Output = `['Ontario Lacus']`

**retrieveFeaturesFromLatitudeLongitudeRange**

Return a list of features found at a range of latitude/longitude positions

```
retrieveFeaturesFromLatitudeLongitudeRange(northernmost_latitude=None,
					southernmost_latitude=None,
					easternmost_longitude=None,
					westernmost_longitude=None)
```
* **[REQUIRED]** northernmost_latitude (float/int): Latitude (in degrees) where North must be greater than or equal to the south, range from -90° to 90°
* **[REQUIRED]** southernmost_latitude (float/int): Latitude (in degrees) where South must be less than or euqal to the north, range from -90° to 90°
* **[REQUIRED]** easternmost_longitude (float/int): Longitude (in degrees) where West must be less than or equal to the east, range from 0° to 360°
* **[REQUIRED]** westernmost_longitude (float/int): Longitude (in degrees) where East must be greater than or equal to the west, range from 0° to 360°

```python
import pydar

pydar.retrieveFeaturesFromLatitudeLongitudeRange(southernmost_latitude=-80,
						northernmost_latitude=-50,
						westernmost_longitude=170,
						easternmost_longitude=190)
```
Output = `'[Crveno Lacus', 'Ontario Lacus', 'Romo Planitia', 'Saraswati Flumen']`

**retrieveIDSByTime**

Retrieve a dictionary of flyby IDs and segment numbers based on a specific timestamp

```
retrieveIDSByTime(year=None,
		doy=None,
		hour=None,
		minute=None,
		second=None,
		millisecond=None)
```
* **[REQUIRED]** year (int): Year for observation, range from 2004 to 2014
* **[REQUIRED]** doy (int): Day of the year, from 0 to 365 (where January 10 = 10) (__Note__: 'doy' not 'day' for days of the year)
* [OPTIONAL] hour (int): Hour, from 0 to 23 in UTC, defaults to 0 when undefined
* [OPTIONAL] minute (int): Minute, from 0 to 59, defaults to check the all minutes when undefined
* [OPTIONAL] second (int): Second, from 0 to 59, defaults to check the all seconds when undefined
* [OPTIONAL] millisecond (int): Milliscond, from 0 to 999, defaults to check all milliseconds when undefined

Where `2004 year, 300 doy, 15 hour, 30 minute, 7 second, 789 millisecond` becomes `2004-300T15:30:07.789`

```python
import pydar
pydar.retrieveIDSByTime(year=2004,
			doy=300,
			hour=15,
			minute=30, 
			second=7, 
			millisecond=789)
```
Output = `{'Ta': ['S01']}`

If hour, minute, second, or millisecond is left undefined, will search the entire range for all possible values and can find more possible ids

For a single day, some flybys have segments that are defined in one large range, but not within a smaller range

```python
import pydar
pydar.retrieveIDSByTime(year=2005, doy=301)
```
Output for the entire day of 301 = `{'T8': ['S02', 'S03', 'S01']}`

```python
import pydar
pydar.retrieveIDSByTime(year=2005, doy=301, hour=3)
```
Output for the day 301 but just for hour 3 = `{'T8': ['S03', 'S01']}` (does not include S02)


**retrieveIDSByTimeRange**

Retrieve a dictionary of flyby IDs and segment numbers based on a start and end datetime

```
retrieveIDSByTimeRange(start_year=None, 
			start_doy=None,
			start_hour=None,
			start_minute=None, 
			start_second=None,
			start_millisecond=None,
			end_year=None, 
			end_doy=None,
			end_hour=None,
			end_minute=None, 
			end_second=None,
			end_millisecond=None)
```

* **[REQUIRED]** start_year (int): Year for observation, range from 2004 to 2014, start_year must be less than/equal to end_year
* **[REQUIRED]** end_year (int): Year for observation, range from 2004 to 2014, end_year must be greater than/equal to start_year
* **[REQUIRED]** start_doy (int): Day of the year, from 0 to 365 (where January 10 = 10) (__Note__: 'doy' not 'day' for days of the year), start_doy must be less than/equal to end_doy
* **[REQUIRED]** end_doy (int): Day of the year, from 0 to 365 (where January 10 = 10) (__Note__: 'doy' not 'day' for days of the year), end_doy must be less than/equal to start_doy
* [OPTIONAL] start_hour (int): Hour, from 0 to 23 in UTC, defaults to check all hours when undefined, start_hour must be less than/equal to end_hour
* [OPTIONAL] end_hour (int): Hour, from 0 to 23 in UTC, defaults to check all hours when undefined, end_hour must be less than/equal to start_hour
* [OPTIONAL] start_minute (int): Minute, from 0 to 59, defaults to check all minutes when undefined, start_minute must be less than/equal to end_minute
* [OPTIONAL] end_minute (int): Minute, from 0 to 59, defaults to check all minutes when undefined, end_minute must be greater than/equal to start_minute
* [OPTIONAL] start_second (int): Second, from 0 to 59, defaults to check all seconds when undefined, start_second must be less than/equal to end_second
* [OPTIONAL] end_second (int): Second, from 0 to 59, defaults to check all seconds when undefined, end_second must be greater than/equal to start_second
* [OPTIONAL] start_millisecond (int): Milliscond, from 0 to 999, defaults to check all milliseconds when undefined, start_millisecond must be less than/equal to end_millisecond
* [OPTIONAL] end_millisecond (int): Milliscond, from 0 to 999, defaults to check all milliseconds when undefined, end_millisecond must be greater than/equal to start_millisecond

```python
import pydar
pydar.retrieveIDSByTimeRange(start_year=2004,
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
				end_millisecond=987):
```
Output = `{'Ta': ['S01'], 'T3': ['S01'], 'T7': ['S01']}`

## Use Downloaded Data
**displayImages**

```
displayImages(image_directory=None)
```

* **[REQUIRED]** image_directory (string): 

Displays downloaded image .IMG files (unzipped from within the .ZIP files) and display all images in directory

```python
import pydar
pydar.displayImages("pydar_results/CORADR_0065_V03_S01")
```
displayImages() will plt.show() all images in the saved results directory

**extractMetadata**

Extract metadata from .TAB file (using .FMT as a reference)

```python
import pydar
pydar.extractMetadata()
```

## TODO:
### TODO Code:
* add a colored outline around a feature when displaying as a 2D image
* save image pixel to an array
* extract pdr functionality to reduce overhead
* displayImages() bug fix: 87 displays invalid integer
* segments will be less than 99 (default to 1 - 01 is the primary imaging)
* progress bars print to command line (still downloading...)
* save .IMG as .SHP for ArcGIS

### TODO Questions:
* add details for what a segement_num is
* associate burst ID from SBDR data to BIDR data for metadata
* save .IMG as an array of pixel values
* save .IMG as .SHP for ArcGIS
* project image onto Titan spheriod
* downloadAdditionalDataTypes() does not have functionality (["ABDR", "ASUM", "LBDR", "STDR"]), decide which files to download

### TODO: Tech Debt
* use README information to gather files for download (save computing, tech debt)
* set up constant config file
* Add functionality for extractFlybyDataImages(): additional_data_types_to_download
* Include URL for access to AAREADME and .LBL readme files
* rm -rf pydar_results/ between runs for clean image output
* research Zenodo

### TODO: Test
* test: pull up all passes that saw Ontario Lacus and colorcode with look angle 
* test: pull beam information and number of looks for each pixel 

## Credits
## Bug and Feature Request

Submit a bug fix, question, or feature request as a [Github Issue](https://github.com/unaschneck/pydar/issues) or to ugschneck@gmail.com/cyschneck@gmail.com
