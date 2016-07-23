from json import load as load_json

from lxml import etree

from Libraries.Feature import Feature
from Libraries.OSMIDGenerator import OSMIDGenerator


class CurbRamp(Feature):
    def __init__(self, curbramps_json):
        """
        Load input curb ramps from json object and schema

        :param curbramps_json: the curb ramps json object
        """
        schema_path = 'Schemas/CurbRamp_Schema.json'
        schema_json = load_json(open(schema_path))
        super().__init__(curbramps_json, schema_json)

    def convert(self):
        """
        Convert curb ramps GeoJSON data to DOM tree, features may be duplicated due to the structure of JSON

        :return: a DOM tree structure which is equivalent to the curb ramps json database
        """
        dom_root = etree.Element('osm')
        self.add_header(dom_root)
        id_generator = OSMIDGenerator()

        for elt in self.json_database['features']:
            if elt['geometry']['type'] == 'Point':
                osm_curbramp = etree.SubElement(dom_root, 'node')
                osm_curbramp.attrib['id'] = str(id_generator.get_next())
                self.__node_common_attribute__(osm_curbramp)
                osm_node = etree.SubElement(dom_root, 'node')
                osm_node.attrib['id'] = str(id_generator.get_next())
                osm_node.attrib['lon'] = str(elt['geometry']['coordinates'][0])
                osm_node.attrib['lat'] = str(elt['geometry']['coordinates'][1])
                self.__node_common_attribute__(osm_node)
                osm_nd = etree.SubElement(osm_curbramp, 'nd')
                osm_nd.attrib['ref'] = osm_node.attrib['id']
                if elt['properties'] is not None:
                    for prop in elt['properties']:
                        osm_tag = etree.SubElement(osm_curbramp, 'tag')
                        osm_tag.attrib['k'] = prop
                        osm_tag.attrib['v'] = str(elt['properties'][prop]).lower()
        return dom_root
