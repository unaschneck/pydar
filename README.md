# PYDAR
![PyPi](https://img.shields.io/pypi/v/pydar)
![license](https://img.shields.io/github/license/unaschneck/pydar)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)

Access and manipulation of CASSINI RADAR images

* Retrieve flyby observation data (.FMT, .TAB, .LBL, .IMG)
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
  |        |         |                           c  = Map projection
  |        |         |                            Q = Oblique cylindrical
  |        |         |                           d  = Map resolution
  |        |         |                            B =   2 pixels/degree
  |        |         |                            D =   8 pixels/degree
  |        |         |                            F =  32 pixels/degree
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
### Cross-Reference Table for Observations and Flybys

The Titan flybys ID is not used in the naming convention for the CORADR filenames. The Titan flyby information is contained in the BIDR filenames and in the VOLDESC.CAT under 'Description' and can be found using the following cross-reference table:
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
....

Full cross reference table avaliable locally as: [cassini_flyby.csv](https://github.com/unaschneck/pydar/blob/main/pydar/data/cassini_flyby.csv)

To convert between a Titan Flyby ID and an observation number: pydar.convertFlybyIDToObservationNumber(flyby_id)
```
### Observation Information as filename
The data filename contains a lot of information about the observation 

EXAMPLE) Filename: "BIBQD05S184_D065_T008S03_V03"

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

To collect flby information and images from a feature on Titan, start by selecting a feature, for example: "Ontario Lacus"

Ontario Lacus was visible in four swath observations: T57, T58, T65, T98 [(Page 163)](https://pds-imaging.jpl.nasa.gov/documentation/Cassini_RADAR_Users_Guide_2nd_Ed_191004_cmp_200421.pdf).

To access flyby of Ontario, first specify a flyby. For this example, Ontario Lacus with the features:

* Titan flyby id: 'T65'
* resolution: 'D' (8 pixels/degree)
* Main imaging segement 1: 'S01'

**extractFlybyDataImages()**

Downloads flby data SBDR: .FMT and .TAB files (for example: [SBDR.FMT](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/SBDR/SBDR.FMT) and [SBDR_15_D087_V03.TAB](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/SBDR/SBDR_15_D087_V03.TAB))

Downloads flyby data BIDR: .LBL and .ZIP files (for example: [BIBQH80N051_D087_T016S01_V03.LBL](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/BIDR/BIBQH80N051_D087_T016S01_V03.LBL) and [BIBQH80N051_D087_T016S01_V03.ZIP](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0087_V03/DATA/BIDR/BIBQH80N051_D087_T016S01_V03.ZIP))

```
extractFlybyDataImages(flyby_observation_num=None,
			flyby_id=None,
			segment_num=None,
			additional_data_types_to_download=[],
			resolution='I',
			top_x_resolutions=None)
```
Either a flby_id (for example: 'T65') or a flby_observation_num (for example: '0065') is required. A flyby_id will be translated into a flby_observation_number to access on the backend and the results will be saved under the observation number. 'T65' will become observation number '0021'

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

extractFlybyDataImages() will retrieve images from PDS website and saves results in a directory labeled 'pydar_results' with the flby obsrevation number, version number, and segement number in the title (for example pydar_results/CORADR_0065_V03_S01)

**convertFlybyIDToObservationNumber**

Converts a Titan Flyby ID (for example: 'T65') to an observation number with front padding ('T65' -> '0211')

``python
convertFlybyIDToObservationNumber(flyby_id)
```
***[REQUIRED/OPTIONAL]** flyby_id (string): a valid flyby ID with prefix 'T'

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
pydar.readLBLREADME(coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
					section_to_print="OBLIQUE_PROJ_X_AXIS_VECTOR")
```
Output = "OBLIQUE_PROJ_X_AXIS_VECTOR   = (0.13498322,0.00221225,-0.99084542)"

To get the sections that are available for printing: returnAllLBLOptions()
```python
import pydar
pydar.returnAllLBLOptions()
```
Line-By-Line Options: ['PDS_VERSION_ID', 'DATA_SET_ID', 'DATA_SET_NAME', 'PRODUCER_INSTITUTION_NAME', 'PRODUCER_ID', 'PRODUCER_FULL_NAME', 'PRODUCT_ID', 'PRODUCT_VERSION_ID', 'INSTRUMENT_HOST_NAME', 'INSTRUMENT_HOST_ID', 'INSTRUMENT_NAME', 'INSTRUMENT_ID', 'TARGET_NAME', 'START_TIME', 'STOP_TIME', 'SPACECRAFT_CLOCK_START_COUNT', 'SPACECRAFT_CLOCK_STOP_COUNT', 'PRODUCT_CREATION_TIME', 'SOURCE_PRODUCT_ID', 'MISSION_PHASE_NAME', 'MISSION_NAME', 'SOFTWARE_VERSION_ID', 'FILE_NAME COMPRESSED', 'RECORD_TYPE COMPRESSED', 'ENCODING_TYPE', 'INTERCHANGE_FORMAT', 'UNCOMPRESSED_FILE_NAME', 'REQUIRED_STORAGE_BYTES', '^DESCRIPTION', 'FILE_NAME UNCOMPRESSED', 'RECORD_TYPE UNCOMPRESSED', 'RECORD_BYTES', 'FILE_RECORDS', 'LABEL_RECORDS', '^IMAGE', 'LINES', 'LINE_SAMPLES', 'SAMPLE_TYPE', 'SAMPLE_BITS', 'CHECKSUM', 'SCALING_FACTOR', 'OFFSET', 'MISSING_CONSTANT', 'NOTE', '^DATA_SET_MAP_PROJECTION', 'MAP_PROJECTION_TYPE', 'FIRST_STANDARD_PARALLEL', 'SECOND_STANDARD_PARALLEL', 'A_AXIS_RADIUS', 'B_AXIS_RADIUS', 'C_AXIS_RADIUS', 'POSITIVE_LONGITUDE_DIRECTION', 'CENTER_LATITUDE', 'CENTER_LONGITUDE', 'REFERENCE_LATITUDE', 'REFERENCE_LONGITUDE', 'LINE_FIRST_PIXEL', 'LINE_LAST_PIXEL', 'SAMPLE_FIRST_PIXEL', 'SAMPLE_LAST_PIXEL', 'MAP_PROJECTION_ROTATION', 'MAP_RESOLUTION', 'MAP_SCALE', 'MAXIMUM_LATITUDE', 'MINIMUM_LATITUDE', 'EASTERNMOST_LONGITUDE', 'WESTERNMOST_LONGITUDE', 'LINE_PROJECTION_OFFSET', 'SAMPLE_PROJECTION_OFFSET', 'OBLIQUE_PROJ_POLE_LATITUDE', 'OBLIQUE_PROJ_POLE_LONGITUDE', 'OBLIQUE_PROJ_POLE_ROTATION', 'OBLIQUE_PROJ_X_AXIS_VECTOR', 'OBLIQUE_PROJ_Y_AXIS_VECTOR', 'OBLIQUE_PROJ_Z_AXIS_VECTOR', 'LOOK_DIRECTION', 'COORDINATE_SYSTEM_NAME', 'COORDINATE_SYSTEM_TYPE']
Section Header Options: ['PRODUCT DESCRIPTION', 'DESCRIPTION OF COMPRESSED AND UNCOMPRESSED FILES', 'POINTERS TO START RECORDS OF OBJECTS IN FILE', 'DESCRIPTION OF OBJECTS CONTAINED IN FILE']

## TODO:
### TODO Code:
* error handling: extract_flyby_data_images
* error_handling: displayImages()
* error_handling: extractMetadata()
* error_handling: readAAREADME()
* bug fix: "NOTE" in .lbl
* Include URL for access to AAREADME and .LBL readme files
* use README information to gather files for download (save computing, tech debt)
* README: read by object (OBJECT -> END_OBJECT) for .LBL and AAREADME
* access flyby information based on latitude longitude (return swath coverage)
* access flyby for a specific point (with a margin of error)

### TODO Questions:
* associate burst ID from SBDR data to BIDR data for metadata
* save .IMG as an array of pixel values
* project image onto Titan spheriod
* Download additional data types as optional arguments using additional_data_types_to_download=[]

### TODO: Tech Debt
* rm -rf pydar_results/ between runs for clean image output
* progress bars print to command line
* research Zenodo

### TODO: Test
* test: pull up all passes that saw Ontario Lacus and colorcode with look angle 
* test: pull beam information and number of looks for each pixel 

## CITATION
If you use this package for your research, please cite it as

