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


def validate_input(json_database, schema_database) -> bool:
    """
    Validate JSON input according to the schema

    :param json_database: the input JSON
    :param schema_database: the schema
    :return: a boolean indicates if the input JSON match the schema
    """
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
    """
    Build the XML DOM tree according to the provided JSON. Nodes might be duplicated due to the structure of JSON.

    :param json_database: the json file which is used to build the DOM
    :return: a DOM tree object contains the exact information which is in the JSON
    """
    try:
        json_in = json.load(json_database)
    except json.decoder.JSONDecodeError:
        click.echo("Input JSON fail to be decoded")
        return False
    dom_root = etree.Element('osm')
    id_generator = OSMIDGenerator()

    for elt in json_in['features']:
        if elt['geometry']['type'] == 'LineString':
            osm_way = etree.SubElement(dom_root, 'way')
            osm_way.attrib['id'] = str(id_generator.get_next())
            osm_way.attrib['user'] = 'TestUSER'
            osm_way.attrib['uid'] = '1'
            osm_way.attrib['visible'] = 'true'
            for coordinate in elt['geometry']['coordinates']:
                osm_node = etree.SubElement(dom_root, 'node')
                osm_node.attrib['id'] = str(id_generator.get_next())
                osm_node.attrib['lon'] = str(coordinate[0])
                osm_node.attrib['lat'] = str(coordinate[1])
                osm_nd = etree.SubElement(osm_way, 'nd')
                osm_nd.attrib['ref'] = osm_node.attrib['id']
            if elt['properties'] is not None:
                for prop_key in elt['properties']:
                    osm_tag = etree.SubElement(osm_way, 'tag')
                    osm_tag.attrib['k'] = prop_key
                    osm_tag.attrib['v'] = str(elt['properties'][prop_key])

    return dom_root


def merge_node(xml_dom, tolerance):
    """
    Merge nodes which are duplicate in a DOM tree

    :param xml_dom: the DOM tree whose nodes need to be merged
    :param tolerance: how close (in degree) should the algorithm consider one node is a duplicate of another
    :return: a DOM tree whose duplicates are merged
    """
    # Sort out all nodes
    nodes = []
    for child in list(xml_dom):
        if child.tag == 'node':
            nodes.append(child)

    # Group nodes when they are close
    nodes_groups = []
    grouped = False
    for node in nodes:
        grouped = False
        for group in nodes_groups:
            for group_member in group:
                if can_group(group_member, node, tolerance):
                    group.append(node)
                    grouped = True
                    break
            if grouped:
                break
        if not grouped:
            nodes_groups.append([node])

    # Merge nodes
    for group in nodes_groups:
        if len(group) > 1:
            for node in group:
                if node != group[0]:
                    substitute_nd_id(xml_dom, group[0], node)

    return xml_dom


def can_group(node_1, node_2, tolerance) -> bool:
    """
    Decide if two nodes can be grouped(and be merged later)

    :param node_1: a node
    :param node_2: another node
    :param tolerance: how close (in degree) should the algorithm consider one node is a duplicate of another
    :return: a boolean indicates if two nodes can be grouped
    """
    if distance(node_1.attrib['lon'], node_2.attrib['lon']) <= tolerance and \
                    distance(node_1.attrib['lat'], node_2.attrib['lat']) <= tolerance:
        return True
    else:
        return False


def distance(num1, num2) -> float:
    """
    Calculate distance of two numbers
    :param num1: a number, do not necessarily have to be a number type
    :param num2: another number, do not necessarily have to be a number type
    :return: a float of their distance
    """
    return abs(float(num1) - float(num2))


def substitute_nd_id(xml_dom, representative_node, substitute_node):
    """
    Search through a DOM tree and merge a node

    :param xml_dom: the DOM tree
    :param representative_node: the node that substitute_node is to be merged to
    :param substitute_node: the node to be merged to representative_node
    :return:
    """
    representative_id = representative_node.attrib['id']
    substitute_id = substitute_node.attrib['id']
    recursive_substitute_nd_id(xml_dom, representative_id, substitute_id)
    substitute_node.getparent().remove(substitute_node)


def recursive_substitute_nd_id(dom_member, representative_id, substitute_id):
    """
    Recursive function which search through a DOM member and substitute the id

    :param dom_member: a member of the DOM tree
    :param representative_id: the id of the node that substitute_id is to be merged to
    :param substitute_id: the id of the node to be merged to representative_id
    :return:
    """
    if dom_member.tag == 'nd' and dom_member.attrib['ref'] == substitute_id:
        dom_member.attrib['ref'] = representative_id

    if len(dom_member.getchildren()) == 0:
        return

    for child in dom_member.getchildren():
        recursive_substitute_nd_id(child, representative_id, substitute_id)


def to_xml(xml_dom, output_path):
    """
    Export the DOM tree to file

    :param xml_dom: the DOM tree which is to be exported
    :param output_path: the path of the exported file
    :return: a boolean indicates if the export progress is successful
    """
    et = etree.ElementTree(xml_dom)
    et.write(output_path, pretty_print=True)
    return True


@click.command()
@click.option('--validate_only', default=False, help='only perform schema validation without conversion')
@click.option('--validate/--no-validate', default=True,
              help='Turn on/off validation of input GeoJSON file before conversion')
@click.option('--tolerance', default=0.001, help='Tolerance when deciding if two close point can be merged'
                                                 '(from 0.00001 to 1, otherwise no merging)')
@click.argument('file_in', type=click.Path(exists=True, readable=True, allow_dash=True))
@click.argument('file_out', type=click.Path(exists=False, writable=True, allow_dash=True))
@click.argument('json_schema', default='Schemas/GlobalOpenSidewalksSchema.json',
                type=click.Path(exists=True, readable=True, allow_dash=True))
def converter(file_in, file_out, json_schema, validate_only, validate, tolerance):
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

    if validate_only:
        click.echo('Validation Complete')
        click.echo('...')
        return

    xml_dom = build_dom(open(file_in))
    if xml_dom is False:
        click.echo('Failed to Read Input File')
        click.echo('Operation Terminated')
        return
    else:
        click.echo('Input File Read Successfully')
        click.echo('...')

    if 0.00001 < tolerance < 1:
        click.echo('Merging(Tolerance: %.4f)' % tolerance)
        merge_node(xml_dom, tolerance)
        click.echo('...')

    if to_xml(xml_dom, file_out):
        click.echo('OSM file saved: %s' % file_out)
        click.echo('...')
    else:
        click.echo('OSM file failed to save')
        click.echo('Operation Terminated')
        return

    click.echo('Operation Complete')
    click.echo('...')


if __name__ == '__main__':
    converter()
