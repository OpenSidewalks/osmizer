# Data Import Tool for Global OpenSidewalks

1. [What is Data Import Tool](#what-is-data-import-tool)
1. [Features](#features)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is Data Import Tool

## Features
- Validate input JSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Merge multiple layers into one
- Deduplicate (default and can be disabled)

## Usage
- To Convert
```
GeoJSONtoOSM.py convert sidewalks <input.json> <output.json>
GeoJSONtoOSM.py convert curbramps <input.json> <output.json>
GeoJSONtoOSM.py convert crossings <input.json> <output.json>
```
- To Validate
```
GeoJSONtoOSM.py validate sidewalks <input.json> <output.json>
GeoJSONtoOSM.py validate curbramps <input.json> <output.json>
GeoJSONtoOSM.py validate crossings <input.json> <output.json>
```
- To Merge
```
GeoJSONtoOSM.py merge <output1.json> <output2.json> <output_final.json>
```

## Options
```
  --validate_only TEXT        only perform schema validation without
                              conversion
  --validate / --no-validate  Turn on/off validation of input GeoJSON file
                              before conversion
  --tolerance FLOAT           Tolerance when deciding if two close point can
                              be merged(from 0.00001 to 1, otherwise no
                              merging)
  --help                      Show this message and exit.
```

## Example Usage
- Conversion
```
python GeoJSONtoOSM.py GeoJSONSamples/AllMergeSample.json out.xml Schemas/GlobalOpenSidewalksSchema.json
running with lxml.etree
File in: GeoJSONSamples/AllMergeSample.json
File out: out.xml
...
Checked: Valid GeoJSON Input File
...
Input File Read Successfully
...
Merging(Tolerance: 0.0010)
...
OSM file saved: out.xml
...
Operation Complete
...
```
- Validation Only
```
python GeoJSONtoOSM.py --validate_only true GeoJSONSamples/AllMergeSample.json out.xml Schemas/GlobalOpenSidewalksSchema.json
running with lxml.etree
File in: GeoJSONSamples/AllMergeSample.json
File out: out.xml
...
Checked: Valid GeoJSON Input File
...
Validation Complete
...
```