import copy
import jsonschema
import click
import sys

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


class Feature:
    def __init__(self, json_database=None, schema=None):
        """
        Load input json object and schema object

        :param json_database: the input json object
        :param schema: the schema json object
        """
        self.json_database = json_database
        self.schema = schema

    def validate(self):
        """
        Validate JSON input according to the schema

        :return: a boolean indicates if the input JSON match the schema
        """
        if self.json_database is None or self.schema is None:
            raise ValueError('JSON input or schema not found')

        json_copy = copy.deepcopy(self.json_database)
        try:
            jsonschema.validate(json_copy, self.schema)
        except jsonschema.ValidationError as err:
            click.echo('Input JSON fail to match schema')
            click.echo('Error:\n')
            click.echo(err)
            return False
        except:
            click.echo('Unexpected error:', sys.exc_info()[0])
            return False

        return True

    def convert(self):
        raise NotImplementedError('Implement convert before use')

    def add_header(self, osm_xml_dom_root):
        osm_xml_dom_root.attrib['version'] = str(0.6)
        osm_xml_dom_root.attrib['generator'] = 'OpenSidewalks Data Import Tool'

    def dedup(self, xml_dom, tolerance):
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
                    if self.__can_group__(group_member, node, tolerance):
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
                        self.__substitute_nd_id__(xml_dom, group[0], node)

        return xml_dom

    def __can_group__(self, node_1, node_2, tolerance) -> bool:
        """
        Decide if two nodes can be grouped(and be merged later)

        :param node_1: a node
        :param node_2: another node
        :param tolerance: how close (in degree) should the algorithm consider one node is a duplicate of another
        :return: a boolean indicates if two nodes can be grouped
        """
        if self.__distance__(node_1.attrib['lon'], node_2.attrib['lon']) <= tolerance and \
                        self.__distance__(node_1.attrib['lat'], node_2.attrib['lat']) <= tolerance:
            return True
        else:
            return False

    def __distance__(self, num1, num2) -> float:
        """
        Calculate distance of two numbers

        :param num1: a number, do not necessarily have to be a number type
        :param num2: another number, do not necessarily have to be a number type
        :return: a float of their distance
        """
        return abs(float(num1) - float(num2))

    def __substitute_nd_id__(self, xml_dom, representative_node, substitute_node):
        """
        Search through a DOM tree and merge a node

        :param xml_dom: the DOM tree
        :param representative_node: the node that substitute_node is to be merged to
        :param substitute_node: the node to be merged to representative_node
        :return:
        """
        representative_id = representative_node.attrib['id']
        substitute_id = substitute_node.attrib['id']
        self.__recursive_substitute_nd_id__(xml_dom, representative_id, substitute_id)
        substitute_node.getparent().remove(substitute_node)

    def __recursive_substitute_nd_id__(self, dom_member, representative_id, substitute_id):
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
            self.__recursive_substitute_nd_id__(child, representative_id, substitute_id)

    def merge(self, dom1, dom2):
        # TODO: Implement merge
        raise NotImplementedError()

    def to_xml(self, xml_dom, output_path):
        """
        Export the DOM tree to file

        :param xml_dom: the DOM tree which is to be exported
        :param output_path: the path of the exported file
        :return: a boolean indicates if the export progress is successful
        """
        et = etree.ElementTree(xml_dom)
        et.write(output_path, pretty_print=True, xml_declaration=True, encoding="utf-8")
        return True
