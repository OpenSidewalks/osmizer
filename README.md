[![Build Status](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool.svg?branch=master)](https://travis-ci.org/OpenSidewalks/DSSG2016-Sidewalks-ImportTool)

# osmizer: GeoJSON -> OSM Import Tool (Developed for Global OpenSidewalks)

1. [What is osmizer](#what-is-osmizer)
1. [Features](#features)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is Dosmizer

## Features
- Validate input JSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Deduplicate (default and can be disabled)
- Merge multiple layers into one

## Usage
```
osmizer [OPTIONS] COMMAND [ARGS]...
```
- Convert
```
osmizer convert sidewalks <input.json> <output.json>
osmizer convert curbramps <input.json> <output.json>
osmizer convert crossings <input.json> <output.json>
```
- Validate
```
osmizer validate sidewalks <input.json>
osmizer validate curbramps <input.json>
osmizer validate crossings <input.json>
```
- Merge
```
osmizer merge <output1.json> <output2.json> <output_final.json>
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
osmizer convert sidewalks GeoJSONSamples/AllMergeSample.json out.xml
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
python osmizer validate sidewalks GeoJSONSamples/AllMergeSample.json
running with lxml.etree
Checked: Valid GeoJSON Input File
...
Operation Finished
...
```
