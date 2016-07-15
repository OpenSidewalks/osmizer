# Data Import Tool for Global OpenSidewalks

1. [What is Data Import Tool](#what-is-data-import-tool)
1. [Features](#features)
1. [Usage](#usage)
    - [Options](#options)

## What is Data Import Tool

## Features
- Turns any Global OpenSidewalks standard schema into OSM standard format
- Validate input JSON format before conversion

## Usage
```
GeoJSONtoOSM.py [OPTIONS] FILE_IN FILE_OUT [VALIDATE_SCHEMA]
```

## Options
```
  --validate / --no-validate  Turn on/off validation the input GeoJSON file
                              before conversion
  --help                      Show this message and exit.
```