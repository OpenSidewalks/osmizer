[![Build Status](https://travis-ci.org/OpenSidewalks/osmizer.svg?branch=master)](https://travis-ci.org/OpenSidewalks/osmizer)

# osmizer: GeoJSON -> OSM Import Tool (Developed for OpenSidewalks)

1. [What is osmizer](#what-is-osmizer)
1. [Features](#features)
1. [Installation](#installation)
1. [Launch the App](#launch-the-app)
1. [Usage](#usage)
    - [Options](#options)
    - [Example Usage](#example-usage)

## What is osmizer
Osmizer is an Python based import tool which converts [OpenSidewalks](https://Opensidewalks.com) specified GeoJSON sidewalks data into OpenStreetMap XML format.

## Features
- Validate input GeoJSON format before conversion
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Deduplicate same geometry points
- Merge multiple layers into one

## Requirement
- The app is only tested on Python 3.4 and 3.5. Therefore, these two versions of Python is recommended to run the application

## Installation
First clone the git repository:
```
git clone --recursive git://github.com/OpenSidewalks/osmizer.git
```
Installing osmizer inside a Python virtual environment is recommended.

To create a virtual environment and install dependencies:
```
cd osmizer
sudo easy_install virtualenv
virtualenv env
./env/bin/pip install -r requirements.txt
```

## Launch the App
After installation, there are two ways to launch the application in Python 3

- From Python 3 directly
    ```
    python3 -m osmizer
    ```

- From modules installed by pip (to install pip, please visit [here](https://pip.pypa.io/en/stable/installing/))
    ```
    pip install osmizer
    osmizer
    ```

## Usage
```
osmizer [OPTIONS] COMMAND [ARGS]...
```
- Convert
```
osmizer convert sidewalks <input.geojson> <output.geojson>
```
```
osmizer convert curbramps <input.geojson> <output.geojson>
```
```
osmizer convert crossings <input.geojson> <output.geojson>
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
python3 -m osmizer convert sidewalks example_data/sidewalk_sample.geojson out.osm
```
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
```
- Validation Only
```
python3 -m osmizer validate sidewalks example_data/sidewalk_sample.geojson
```
```
Checked: Valid GeoJSON Input File
...
Operation Finished
...
```
