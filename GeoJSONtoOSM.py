import click
import json
import jsonschema
import sys
from OSMIDGenerator import OSMIDGenerator

# import lxml etree
try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")


def validate_input(json_database, schema_database):
    try:
        json_in = json.load(json_database)
        schema_in = json.load(schema_database)
        jsonschema.validate(json_in, schema_in)
    except json.decoder.JSONDecodeError:
        click.echo("Input JSON fail to be decoded")
        return False
    except jsonschema.ValidationError:
        click.echo("Input JSON fail to match schema")
        return False
    except:
        click.echo("Unexpected error:", sys.exc_info()[0])
        return False

    return True


def build_dom(json_database):
    try:
        json_in = json.load(json_database)
    except json.decoder.JSONDecodeError:
        click.echo("Input JSON fail to be decoded")
        return False
    dom_root = etree.Element('osm')
    id_generator = OSMIDGenerator()
    # TODO: Turns json input to DOM tree
    return False


def to_OSM(gpd_database, output_path):
    # TODO: Output file to OSM format
    return False


@click.command()
@click.option('--validate/--no-validate', default=True,
              help='Turn on/off validation the input GeoJSON file before conversion')
@click.argument('file_in', type=click.Path(exists=True, readable=True, allow_dash=True))
@click.argument('file_out', type=click.Path(exists=False, writable=True, allow_dash=True))
@click.argument('json_schema', default='Schemas/SampleJSONSchema.json',
                type=click.Path(exists=True, readable=True, allow_dash=True))
def converter(file_in, file_out, validate, json_schema):
    click.echo('File in: ' + file_in)
    click.echo('File out: ' + file_out)
    click.echo('...')

    if validate:
        if validate_input(open(file_in), open(json_schema)):
            click.echo('Checked: Valid GeoJSON Input File')
            click.echo('...')
        else:
            click.echo('ERROR: Non-Valid GeoJSON Input File')
            click.echo('Operation Terminated')
            return

    xml_dom = build_dom(open(file_in))
    if not xml_dom:
        click.echo('Failed to Read Input File')
        click.echo('Operation Terminated')
        return
    else:
        click.echo('Input File Read Successfully')
        click.echo('...')

    if to_OSM(xml_dom, file_out):
        click.echo('OSM file saved')
        click.echo('...')
    else:
        click.echo('OSM file failed to save')
        click.echo('Operation Terminated')
        return

    click.echo('Operation Complete')


if __name__ == '__main__':
    converter()
