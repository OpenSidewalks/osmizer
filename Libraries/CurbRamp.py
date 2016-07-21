from Libraries import Feature
from Libraries.OSMIDGenerator import OSMIDGenerator
from lxml import etree
from json import load as load_json

class CurbRamp(Feature.Feature):
    def __init__(self, curbramps_json):
        super().__init__(curbramps_json)

    def convert(self):
        """
        Convert curb ramps GeoJSON data to DOM tree, features may be duplicated due to the structure of JSON

        :return: a DOM tree structure which is equivalent to the curb ramps json database

         """
        # TODO: Implement convert
        dom_root = etree.Element('osm')
        self.add_header(dom_root)
        id_generator = OSMIDGenerator()

        for elt in self.json_database['features']:
            if elt['geometry']['type'] == "Point":
                osm_curbramp = etree.SubElement(dom_root, 'node')
                osm_curbramp.attrib['id'] = str(id_generator.get_next())
                osm_node = etree.SubElement(dom_root, 'node')
                osm_node.attrib['id'] = str(id_generator.get_next())
                osm_node.attrib['lon'] = str(elt['geometry']['coordinates'][0])
                osm_node.attrib['lat'] = str(elt['geometry']['coordinates'][1])
                osm_nd = etree.SubElement(osm_curbramp, 'nd')
                osm_nd.attrib['ref'] = osm_node.attrib['id']
                if elt['properties'] is not None:
                    for property in elt['properties']:
                        osm_tag = etree.SubElement(osm_curbramp, 'tag')
                        osm_tag.attrib['k'] = property
                        osm_tag.attrib['v'] = str(elt['properties'][property])
        return dom_root

