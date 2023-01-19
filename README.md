# PYDAR
![PyPi](https://img.shields.io/pypi/v/pydar)
![license](https://img.shields.io/github/license/unaschneck/pydar)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)

Python Package to access and manipulate CASSINI RADAR images in one place

* Find relevant flyby observation numbers and IDs for a specific region, feature, or location
* Retrieve flyby observation data (.FMT, .TAB, .LBL, .IMG) from SBDR and BIDR by default
* Access AAREADME and .LBL readme information
* Display PDS image retrieved for flyby observation

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
Download time varies depending on the number and size of files of interest. On average, most single feature downloads take between 2-5 minutes to download.

![image](https://user-images.githubusercontent.com/24469269/211881026-5bab329c-cf0d-416b-bedc-6d466b77b1f5.png)
([Cassini Radar Volume SIS, Version 2.1](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0284/DOCUMENT/VOLSIS.PDF) Table 1, pg. 3)
### Cross-Reference Table for Observations and Flybys
The Titan flybys ID is not used in the naming convention for the CORADR filenames. The Titan flyby information is contained in the BIDR filenames and in the VOLDESC.CAT under 'Description' and can be found using the following cross-reference table: [cassini_flyby.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/cassini_flyby.csv)

```
Flyby ID Cross Reference Table
Prime Mission and Extended Mission

Column 1: Titan flyby id
Column 2: Radar Data Take Number
Column 3: Sequence number
Column 4: Orbit Number/ID

Ta   DTN 035   S05 Rev 0A
T3   DTN 045   S08 Rev 03
T4   DTN 048   S09 Rev 04
T7   DTN 059   S14 Rev 14
T8   DTN 065   S15 Rev 17

...
```

To convert between a Titan Flyby ID and an observation number: `pydar.convertFlybyIDToObservationNumber(flyby_id)`

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

BIBQD05S184_D065_T008S03_V03.JPG:

![BIFQI10S251_D065_T008S01_V03](https://user-images.githubusercontent.com/24469269/210164143-427003ed-0043-45b4-a80f-8e9ddf28543a.jpg)

### Volume Version of Data

Some passes have multiple versions of the data.

* Version 1 (V01) was the first archived version of the data and assumed Titan had zero obliquity, which resulted in misregistration between passes

* Version 2 (V02) used a Titan spin model that reduced misregistration error 

* Version 3 (V03) used a long-term, accurate spin model for Titan along with other improvements

Only some Titan passes produced all of the version numbers.

* TA-T25 : V01, V02, V03

* $\gt$ T28: V02, V03

* T108-T126: labeled only once as V02 but is actually V03

The version number is listed in the filenanme and in VOLDESC.CAT under the 'VOLUME_VERSION_ID'

*Version 3 is the latest and preferred version*

Example:

Version 1 is named BIFQI48N071_D035_T00A_V01.IMG

Version 2 is named BIFQI49N071_D035_T00AS01_V02.IMG

Version 3 is named BIFQI49N071_D035_T00AS01_V03.IMG

### Segment Number of Data
A single flyby can produce multiple image segments (Sxx). *S01 is the primary imaging segment* with other segments referring to periods in the flyby when the instrument went to/from altimetry/SAR/HiSAR or weird pointing profiles.  

![image](https://user-images.githubusercontent.com/24469269/210197286-c059ffed-281d-46c7-911a-f86c3bf7ea28.png)
Credit: Cassini Radar User Guide (Wall et al. 2019, pg.16)
## Documentation

## Data Files

**feature_name_details.csv**

List of Features on Titan with names with their associated position and the origin of their name. Taken from the [planetarynames.wr.usgs.gov](https://planetarynames.wr.usgs.gov/Feature/6981)

## SBDR Files
[SBDR column descriptions](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0045/DOCUMENT/BODPSIS.PDF)

Total width of the RADAR swath is created by combining the five individual sub-swaths, where the center beam is the highest gain
![image](https://user-images.githubusercontent.com/24469269/211431884-c201ac74-114a-4c17-b95a-f9edf0178d2e.png)
(_The Cassini Huygens Mission: Orbiter Remote Sensing Observation 2004_)

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
Python 3.9
```
pip3 install -r requirements.txt
```
## Install
PyPi pip install at [pypi.org/project/pydar/](https://pypi.org/project/pydar/)

```
pip install pydar
```

## Examples

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
Output = `{'T36': ['S03'], 'T39': ['S06', 'S05', 'S01', 'S04'], 'T48': ['S04'], 'T49': ['S01'], 'T50': ['S02'], 'T55': ['S01', 'S03'], 'T56': ['S01'], 'T57': ['S01', 'S02'], 'T58': ['S01'], 'T59': ['S01'], 'T65': ['S04', 'S01', 'S05', 'S02', 'S03'], 'T71': ['S01'], 'T95': ['S03'], 'T98': ['S01', 'S04']}`

**retrieveIDSByLatitudeLongitude**

Retrieve a list of flyby IDs with their associated segments based on specific latitude and longitude

```python
retrieveIDSByLatitudeLongitude(latitude=None, longitude=None)
```
* **[REQUIRED]** latitude (float/int): Latitude (in degrees) where North = + and South = -
* **[REQUIRED]** longitude (float/int): Longitude (in degrees) where West = + and East = -

```python
import pydar
pydar.retrieveIDSByLatitudeLongitude(latitude=10, longitude=10)
```
Output = `{'T19': ['S01'], 'T29': ['S01'], 'T55': ['S01'], 'T56': ['S01'], 'T57': ['S01'], 'T58': ['S01'], 'T64': ['S01'], 'T83': ['S02'], 'T84': ['S02'], 'T92': ['S01'], 'T98': ['S02'], 'T104': ['S01']}`

**retrieveIDSByLatitudeLongitudeRange**

```python
retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=None,
				southernmost_latitude=None,
				easternmost_longitude=None,
				westernmost_longitude=None)
```
* **[REQUIRED]** northernmost_latitude (float/int): Latitude (in degrees) where North = + and South = -, north must be greater than or equal to the south
* **[REQUIRED]** southernmost_latitude (float/int): Latitude (in degrees) where North = + and South = -, south must be less than or euqal to the north
* **[REQUIRED]** easternmost_longitude (float/int): Longitude (in degrees) where West = + and East = -, west must be less than or equal to the east
* **[REQUIRED]** westernmost_longitude (float/int): Longitude (in degrees) where West = + and East = -, east must be greater than or equal to the west

```python
retrieveIDSByLatitudeLongitudeRange(northernmost_latitude=15,
				southernmost_latitude=10,
				easternmost_longitude=12,
				westernmost_longitude=17)
```
Output = `{'T19': ['S01'], 'T29': ['S01'], 'T55': ['S01'], 'T56': ['S01'], 'T57': ['S01'], 'T64': ['S01'], 'T83': ['S02'], 'T84': ['S02'], 'T92': ['S01'], 'T98': ['S02'], 'T104': ['S01']}`

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
* **[REQUIRED]** segment_num (string): 
* [OPTIONAL] additional_data_types_to_download (List of Strings): Possible options ["ABDR", "ASUM", "BIDR", "LBDR", "SBDR", "STDR"]
* [OPTIONAL] resolution (String): resolution options "B", "D", "F", "H", or "I" (2, 8, 32, 128, 256 pixels/degree), defaults to highest resolution 'I'
* [OPTIONAL] top_x_resolutions: Save the top x resolution types (5 total resolutions)


```python
import pydar

# Extract Flyby Data Files to pydar_results/ directory: 
pydar.extractFlybyDataImages(flyby_id='T65', resolution='D', segment_num="S01", additional_data_types_to_download=["STDR", "LBDR"])
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

observation_number = convertFlybyIDToObservationNumber(flyby_id)
```

Observation number based on the 'Radar Data Take Number' in the cassini_flyby.csv file with front padding to ensure that all observation numbers are 4 digits long (0065 and 0211)

Requires each Titan flyby ID to be a valid value the cassini_flyby.csv 

**displayImages**

```
displayImages(image_directory=None)
```

* **[REQUIRED]** image_directory (string): 

Displays downloaded image .IMG files (unzipped from within the .ZIP files)

```python
import pydar
# Display all Images in pydar_results/ directory
pydar.displayImages("pydar_results/CORADR_0065_V03_S01")
```
displayImages() will plt.show() all images in the saved results directory

**extractMetadata**

Extract metadata from .TAB file (using .FMT as a reference)

```python
import pydar
# Extract Metadata from .FMT and .TAB files
pydar.extractMetadata()
```

**readAAREADME**

Print AAREADME.TXT to console for viewing

```
readAAREADME(coradr_results_directory=None,
			section_to_print=None, 
			print_to_console=True)
```

* **[REQUIRED]** coradr_results_directory (string):
* [OPTIONAL] section_to_print (string): Specify a section to print to console from the AAREADME, defaults to print the entire AAREADME.TXT (readme options: ['PDS_VERSION_ID', 'RECORD_TYPE', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_NAME', 'OBJECT', 'PUBLICATION_DATE', 'NOTE', 'END_OBJECT', 'Volume', 'Introduction', 'Disk Format', 'File Formats', 'Volume Contents', 'Recommended DVD Drives and Driver Software', 'Errata and Disclaimer', 'Version Status', 'Contact Information'])
* [OPTIONAL] print_to_console (boolean): Print to console, defaults to true, otherwise function will return output as a string

```python
import pydar
# Print AAREADME.TXT
pydar.readAAREADME(coradr_results_directory="pydar_results/CORADR_0065_V03_S01",
						section_to_print="Volume")
```
Output = "Volume CORADR_0065:  Titan Flyby T8, Sequence S15, Oct 27, 2005"

To get the section that are avaiable for printing: returnAllAAREADMEOptions()

```python
import pydar
pydar.returnAllAAREADMEOptions()
```

['PDS_VERSION_ID', 'RECORD_TYPE', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_NAME', 'PUBLICATION_DATE', 'NOTE', 'END_OBJECT', 'Volume', 'Introduction', 'Disk Format', 'File Formats', 'Volume Contents', 'Recommended DVD Drives and Driver Software', 'Errata and Disclaimer', 'Version Status', 'Contact Information']

**readLBLREADME**

Print .LBL README to console for viewing

```
readLBLREADME(coradr_results_directory=None,
			section_to_print=None, 
			print_to_console=True)
```

* **[REQUIRED]** coradr_results_directory (string):
* [OPTIONAL] section_to_print (string): Specify a section to print to console from the AAREADME, defaults to print the entire AAREADME.TXT (readme options: ['PDS_VERSION_ID', 'RECORD_TYPE', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_NAME', 'OBJECT', 'PUBLICATION_DATE', 'NOTE', 'END_OBJECT', 'Volume', 'Introduction', 'Disk Format', 'File Formats', 'Volume Contents', 'Recommended DVD Drives and Driver Software', 'Errata and Disclaimer', 'Version Status', 'Contact Information'])
* [OPTIONAL] print_to_console (boolean): Print to console, defaults to true, otherwise function will return output as a string

```python
import pydar
# Print .LBL README
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
* **[REQUIRED]** latitude (float/int): Latitude (in degrees) where North = + and South = -
* **[REQUIRED]** longitude (float/int): Longitude (in degrees) where West = + and East = -

```python
import pydar
feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitude(latitude=-72, longitude=183)
```

feature_names_list = `['Ontario Lacus']`

**retrieveFeaturesFromLatitudeLongitudeRange**

```
retrieveFeaturesFromLatitudeLongitudeRange(northernmost_latitude=None,
										southernmost_latitude=None,
										easternmost_longitude=None,
										westernmost_longitude=None)
```
* **[REQUIRED]** northernmost_latitude (float/int): Latitude (in degrees) where North = + and South = -, north must be greater than or equal to the south
* **[REQUIRED]** southernmost_latitude (float/int): Latitude (in degrees) where North = + and South = -, south must be less than or euqal to the north
* **[REQUIRED]** easternmost_longitude (float/int): Longitude (in degrees) where West = + and East = -, west must be less than or equal to the east
* **[REQUIRED]** westernmost_longitude (float/int): Longitude (in degrees) where West = + and East = -, east must be greater than or equal to the west

```python
import pydar
feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitudeRange(northernmost_latitude=11,
																southernmost_latitude=-80,
																easternmost_longitude=339,
																westernmost_longitude=341)
```
feature_names_list = `['Aaru', 'Rossak Planitia']`

## TODO:
### TODO Code:
* function to return all valid feature names based on a specific or a range of lat/long
* retrieveIDSByTime()
* add a colored outline around a feature when displaying as a 2D image
* segments will be less than 99 (default to 1 - 01 is the primary imaging)
* README for all the functions and their sections
* progress bars print to command line (still downloading...)

### TODO Questions:
* get longitude values when greater than 180 (everything is relative to west)
* add details for what a segement_num is
* associate burst ID from SBDR data to BIDR data for metadata
* save .IMG as an array of pixel values
* save .IMG as .SHP for ArcGIS
* project image onto Titan spheriod
* downloadAdditionalDataTypes() does not have functionality (["ABDR", "ASUM", "LBDR", "STDR"]), decide which files to download

### TODO: Tech Debt
* use README information to gather files for download (save computing, tech debt)
* CSV script to be run before each pypi package update by developer not user
* make README options for .LBL and AAREADME case-insensitive
* set up constant config file
* bug fix: "NOTE" in .lbl
* Include URL for access to AAREADME and .LBL readme files
* rm -rf pydar_results/ between runs for clean image output
* research Zenodo

### TODO: Test
* test: pull up all passes that saw Ontario Lacus and colorcode with look angle 
* test: pull beam information and number of looks for each pixel 

## Bug and Feature Request

Submit a bug fix, question, or feature request as a [Github Issue](https://github.com/unaschneck/pydar/issues) or to ugschneck@gmail.com/cyschneck@gmail.com
