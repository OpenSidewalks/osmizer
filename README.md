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
- Convert
```
osmizer convert sidewalks <input.geojson> <output.geojson>
osmizer convert curbramps <input.geojson> <output.geojson>
osmizer convert crossings <input.geojson> <output.geojson>
```
- Validate
```
osmizer validate sidewalks <input.geojson>
osmizer validate curbramps <input.geojson>
osmizer validate crossings <input.geojson>
```
- Merge
```
osmizer merge <output1.geojson> <output2.geojson> <output_final.geojson>
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
```
- Validation Only
```
python3 osmizer validate sidewalks example_data/sidewalk_sample.geojson
Checked: Valid GeoJSON Input File
...
Operation Finished
...
```
