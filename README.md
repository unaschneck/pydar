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
T13  DTN 082   S20 Rev 23
T15  DTN 086   S21 Rev 25
T16  DTN 087   S22 Rev 26
T17  DTN 093   S23 Rev 28
T18  DTN 098   S24 Rev 29
T19  DTN 100   S24 Rev 30
T20  DTN 101   S25 Rev 31
T21  DTN 108   S26 Rev 35
T23  DTN 111   S27 Rev 37
T25  DTN 120   S28 Rev 39
T28  DTN 126   S29 Rev 42
T29  DTN 127   S29 Rev 43
T30  DTN 131   S30 Rev 44
T36  DTN 149   S34 Rev 50
T39  DTN 157   S36 Rev 54
T41  DTN 161   S38 Rev 59
T43  DTN 166   S40 Rev 67
T44  DTN 167   S40 Rev 69
T48  DTN 174   S46 Rev 95
T49  DTN 177   S46 Rev 97
T50  DTN 181   S47 Rev 102
T52  DTN 186   S49 Rev 107
T53  DTN 189   S49 Rev 109
T55  DTN 193   S50 Rev 111
T56  DTN 195   S50 Rev 112
T57  DTN 199   S51 Rev 113
T58  DTN 200   S51 Rev 114
T59  DTN 201   S52 Rev 115
T61  DTN 203   S53 Rev 117
T63  DTN 209   S55 Rev 122
T64  DTN 210   S56 Rev 123	
T65  DTN 211   S56 Rev 124
T69  DTN 218   S60 Rev 132
T71  DTN 220   S61 Rev 134
T77  DTN 229   S68 Rev 149
T80  DTN 234   S71 Rev 159
T83  DTN 239   S73 Rev 166
T84  DTN 240   S73 Rev 167
T86  DTN 243   S75 Rev 172
T91  DTN 248   S78 Rev 190
T92  DTN 250   S79 Rev 194
T95  DTN 253   S80 Rev 198
T98  DTN 257   S82 Rev 201
T104 DTN 261   S85 Rev 207
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

### Volume version of data

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

### Segment number of data
A single flyby can produce multiple image segments (Sxx). *S01 is the primary imaging segment* with other segments referring to periods in the flyby when the instrument went to/from altimetry/SAR/HiSAR or weird pointing profiles.  

![image](https://user-images.githubusercontent.com/24469269/210197286-c059ffed-281d-46c7-911a-f86c3bf7ea28.png)
Credit: Cassini Radar User Guide (Wall et al. 2019, pg.16)
## Documentation

## SBDR Files
[SBDR column descriptions](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0045/DOCUMENT/BODPSIS.PDF)
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
						resolution='I',
						top_x_resolutions=None)
```
Either a flby_id (for example: 'T65') or a flby_observation_num (for example: '0065') is required. A flyby_id will be translated into a flby_observation_number to access on the backend and the results will be saved under the observation number. 'T65' will become observation number '0021'

* [REQUIRED/OPTIONAL] flyby_observation_num (string): required if flyby_id not included
* [REQUIRED/OPTIONAL] flyby_id (string): required if flyby_observation_num not included
* [REQUIRED] segment_num (String): 
* [OPTIONAL] resolution (String): "B", "D", "F", "H", or "I (2, 8, 32, 128, 256 pixels/degree), defaults to highest resolution 'I'
* [OPTIONAL] top_x_resolutions: Save the top x resolution types (5 total resolutions)


```python
import pydar

# Extract Flyby Data Files to results/ directory: 
pydar.extractFlybyDataImages(flyby_id='T65', resolution='D', segment_num="S01")
```

extractFlybyDataImages() will retrieve images from PDS website and saves results in a directory labeled 'results' with the flby obsrevation number, version number, and segement number in the title (for example results/CORADR_0065_V03_S01)

**displayImages**

```
displayImages(image_directory=None)
```

* [REQUIRED] image_directory (string): 

Displays downloaded image .IMG files (unzipped from within the .ZIP files)

```python
import pydar
# Display all Images in results/ directory
pydar.displayImages("results/CORADR_0065_V03_S01")
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
readAAREADME(coradr_results_directory=None)
```

* [REQUIRED]: coradr_results_directory


```python
import pydar
# Print AAREADME.TXT
pydar.readAAREADME("results/CORADR_0065_V03_S01")
```

## TODO Next:
* Print AAREADME to command line or specify a specific search feature? (from include access to readme from command line)
* make pandas df of all radar data
* associate burst ID from SBDR data to BIDR data for metadata
* save .IMG as an array of pixel values
* include access to lbl file attributes from command line
* project image onto Titan spheriod

## TODO: Tech Debt
* rm -rf results/ between runs for clean image output
* error handling: extract_flyby_data_images
* error_handling: displayImages()
# error_handling: extractMetadata()
* progress bars print to command line
* Zenodo

## TODO: Test
* test: pull up all passes that saw Ontario Lacus and colorcode with look angle 
* test: pull beam information and number of looks for each pixel 

## CITATION
If you use this package for your research, please cite it as

