[![Build Status](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool.svg?branch=master)](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool)

# Data Import Tool for Global OpenSidewalks

[![Build Status](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool.svg?branch=Developing)](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool)

1. [What is Data Import Tool](#what-is-data-import-tool)
1. [Features](#features)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is Data Import Tool

## Features
- Validate input JSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Deduplicate (default and can be disabled)
- Merge multiple layers into one

## Usage
```
GeoJSON2OSM.py [OPTIONS] COMMAND [ARGS]...
```
- Convert
```
GeoJSONtoOSM.py convert sidewalks <input.json> <output.json>
GeoJSONtoOSM.py convert curbramps <input.json> <output.json>
GeoJSONtoOSM.py convert crossings <input.json> <output.json>
```
- Validate
```
GeoJSONtoOSM.py validate sidewalks <input.json>
GeoJSONtoOSM.py validate curbramps <input.json>
GeoJSONtoOSM.py validate crossings <input.json>
```
- Merge
```
GeoJSONtoOSM.py merge <output1.json> <output2.json> <output_final.json>
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
python GeoJSONtoOSM.py convert sidewalks GeoJSONSamples/AllMergeSample.json out.xml
running with lxml.etree
Input File Read Successfully
...
Running Deduplicate(Tolerance: 0.0010)
...
OSM file saved: out.xml
...
Operation Finished
...
```
- Validation Only
```
python GeoJSONtoOSM.py validate sidewalks GeoJSONSamples/AllMergeSample.json
running with lxml.etree
Checked: Valid GeoJSON Input File
...
Operation Finished
...
```
