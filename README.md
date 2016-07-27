[![Build Status](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool.svg?branch=master)](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool)

# Data Import Tool for Global OpenSidewalks

1. [What is Data Import Tool](#what-is-data-import-tool)
1. [Features](#features)
1. [System Requirement](#system-requirement)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is Data Import Tool

## Features
- Validate input JSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Deduplicate (default but can be disabled)
- Merge multiple layers into one

## System Requirement
- Python: Python 3.3 or above
- Click: 6.6 or above
- jsonschema: 2.5.1 or above
- lxml: 3.6.0 or above
- pip: 7.1.0 or above
- setuptools: 18.1 or above
Note: Requirements above are recommended, other versions are not yet tested

## Usage
```
GeoJSON2OSM.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert
  merge
  validate
```
- Convert
    - Convert can only be done on project standard GeoJSON files
```
GeoJSONtoOSM.py convert sidewalks <input.json> <output.json>
GeoJSONtoOSM.py convert curbramps <input.json> <output.json>
GeoJSONtoOSM.py convert crossings <input.json> <output.json>
```
- Validate
    - Validate can only be done on project standard GeoJSON files
```
GeoJSONtoOSM.py validate sidewalks <input.json>
GeoJSONtoOSM.py validate curbramps <input.json>
GeoJSONtoOSM.py validate crossings <input.json>
```
- Merge
    - Merge can only be done on OSM XML files that converted from this tool
```
GeoJSONtoOSM.py merge <output1.osm> <output2.osm> <output_final.osm>
```

## Options
- Convert
```
    --tolerance FLOAT           Change tolerance for deduplicate operation
```
- Validate
- Merge

## Example Usage
- Conversion
```
python3 GeoJSONtoOSM.py convert --tolerance 0.1000 sidewalks GeoJSONSamples/Sidewalks_Merge_Sample.json out.osm
running with lxml.etree
...
Data Import Tool for OpenSidewalks Project
Data Science and Social Good
Taskar Center of Accessible Technology
University of Washington
...
Input File Read Successfully
...
Running Deduplicate(Tolerance: 0.1000)
...
OSM file saved: out.xml
...
Operation Finished
...
```
- Validation Only
```
python3 GeoJSONtoOSM.py validate sidewalks GeoJSONSamples/AllMergeSample.json
running with lxml.etree
...
Data Import Tool for OpenSidewalks Project
Data Science and Social Good
Taskar Center of Accessible Technology
University of Washington
...
Checked: Valid GeoJSON Input File
...
Operation Finished
...
```
