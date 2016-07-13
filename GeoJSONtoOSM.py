import geopandas as gpd
import fiona
import click
import json
import jsonschema
import sys


def validate_input(json_file, schema_file):
    try:
        json_in = json.load(json_file)
        schema_in = json.load(schema_file)
        jsonschema.validate(json_in, schema_in)
    except json.decoder.JSONDecodeError:
        click.echo("Input JSON fail to be decoded")
        return False
    except jsonschema.ValidationError:
        click.echo("Input JSON fail to match schema")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return False

    return True


def read_input(json_path):
    try:
        file_read = gpd.read_file(json_path, mode='r', driver='GeoJSON')
    except fiona.errors.FionaValueError:
        click.echo('Failed to read as GeoJSON')
        return -1
    return file_read


def to_OSM(gpd_database, output_path):
    # TODO: Output file to OSM format
    return True


@click.command()
@click.option('--validate/--no-validate', default=True,
              help='Validate the input GeoJSON file before conversion')
@click.argument('file_in', type=click.Path(exists=True, readable=True, allow_dash=True))
@click.argument('file_out', type=click.Path(exists=False, writable=True, allow_dash=True))
@click.argument('validate_schema', default='Schema/GeoJSONSchema.json',
                type=click.Path(exists=True, readable=True, allow_dash=True))
def converter(file_in, file_out, validate, validate_schema):
    click.echo('File in: ' + file_in)
    click.echo('File out: ' + file_out)
    click.echo('...')

    if validate:
        if validate_input(open(file_in), open(validate_schema)):
            click.echo('Checked: Valid GeoJSON Input File')
            click.echo('...')
        else:
            click.echo('ERROR: Non-Valid GeoJSON Input File')
            click.echo('Operation Terminated')
            return

    database = read_input(file_in)
    if database == -1:
        click.echo('Failed to Read Input File')
        click.echo('Operation Terminated')
        return
    else:
        click.echo('Input File Read Successfully')
        click.echo('...')

    if to_OSM(database, file_out):
        click.echo('OSM file saved')
        click.echo('...')
    else:
        click.echo('OSM file failed to save')
        click.echo('Operation Terminated')
        return

    click.echo('Operation Complete')


if __name__ == '__main__':
    converter()
