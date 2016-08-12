from click import progressbar
from lxml import etree

from osmizer import schemas
from osmizer.features.feature import Feature
from osmizer.idgenerator import OSMIDGenerator


class Sidewalk(Feature):
    def __init__(self, sidewalks_json):
        '''Load input sidewalks json object and schema.

        :param sidewalks_json: the sidewalks json object.

        '''
        schema_json = schemas.load_schema('sidewalk')
        super().__init__(sidewalks_json, schema_json)

    def convert(self):
        '''Convert sidewalks GeoJSON data to DOM tree, features may be
        duplicated due to the structure of JSON.

        :return: a DOM tree structure which is equivalent to the sidewalks
        json database.

        '''
        dom_root = etree.Element('osm')
        self.add_header(dom_root)
        id_generator = OSMIDGenerator()

        # TODO: Add support for polygon
        with progressbar(length=len(self.json_database['features']), label='Converting') as bar:
            for elt in self.json_database['features']:
                if elt['geometry']['type'] == 'LineString':
                    osm_sidewalk = etree.SubElement(dom_root, 'way')
                    osm_sidewalk.attrib['id'] = str(id_generator.get_next())
                    self.__way_common_attribute__(osm_sidewalk)
                    for coordinate in elt['geometry']['coordinates']:
                        osm_node = etree.SubElement(dom_root, 'node')
                        osm_node.attrib['id'] = str(id_generator.get_next())
                        osm_node.attrib['lon'] = str(coordinate[0])
                        osm_node.attrib['lat'] = str(coordinate[1])
                        self.__node_common_attribute__(osm_node)
                        osm_nd = etree.SubElement(osm_sidewalk, 'nd')
                        osm_nd.attrib['ref'] = osm_node.attrib['id']
                    if elt['properties'] is not None:
                        for prop in elt['properties']:
                            osm_tag = etree.SubElement(osm_sidewalk, 'tag')
                            osm_tag.attrib['k'] = prop
                            osm_tag.attrib['v'] = str(elt['properties'][prop]).lower()
                bar.update(1)
            bar.finish()

        return dom_root
