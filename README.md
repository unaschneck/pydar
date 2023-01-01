# PYDAR
![PyPi](https://img.shields.io/pypi/v/pydar)
![license](https://img.shields.io/github/license/unaschneck/pydar)

Access and manipulation of CASSINI RADAR images

## Overview
```
Cassini RADAR Information (CORADR_xxxx): https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/
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
```
** Cross-Reference Table for Observations and Flybys**

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

**Observation Information as filename**

File Name Example: "BIBQD05S184_D065_T008S03_V03"

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

## Documentation

## Dependencies
Python 3.7
```
pip3 install -r requirements.txt
```
## Install
PyPi pip install at [pypi.org/project/pydar/](https://pypi.org/project/pydar/)

```
pip install pydar
```

## Examples

## Tests

## TODO:


