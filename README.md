[![Build Status](https://travis-ci.org/OpenSidewalks/osmizer.svg?branch=master)](https://travis-ci.org/OpenSidewalks/osmizer)

# osmizer: GeoJSON -> OSM Import Tool (Developed for Global OpenSidewalks)

1. [What is osmizer](#what-is-osmizer)
1. [Features](#features)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is osmizer

## Features
- Validate input JSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Deduplicate (default and can be disabled)
- Merge multiple layers into one

## Usage
```
osmizer [OPTIONS] COMMAND [ARGS]...
```
- Validate
```
osmizer validate sidewalks <input.geojson>
```
```
osmizer validate curbramps <input.geojson>
```
```
osmizer validate crossings <input.geojson>
```
- Convert
```
osmizer convert sidewalks <input.json> <output.json>
```
```
osmizer convert curbramps <input.json> <output.json>
```
```
osmizer convert crossings <input.json> <output.json>
```
- Merge
```
osmizer merge <output1.osm> <output2.osm> <output_final.osm>
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
python3 osmizer convert sidewalks example_data/sidewalk_sample.geojson out.osm
```
Converting Input File
Converting  [####################################]  100%
...
Deduping Output(Tolerance: 0.00000010)
Sorting  [####################################]  100%
Building Map  [####################################]  100%
Deduping  [####################################]  100%
...
OSM File Saved as out.osm
...
Operation Finished
...

- Validation Only
```
python3 osmizer validate sidewalks example_data/sidewalk_sample.geojson
```
Checked: Valid GeoJSON Input File
...
Operation Finished
...

