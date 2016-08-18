from click import progressbar
from lxml import etree

from osmizer import schemas
from osmizer.features.feature import Feature
from osmizer.idgenerator import OSMIDGenerator


class CurbRamp(Feature):
    def __init__(self, curbramps_json):
        '''Load input curb ramps from json object and schema.

        :param curbramps_json: the curb ramps json object.

        '''
        schema_json = schemas.load_schema('curbramp')
        super().__init__(curbramps_json, schema_json)

    def convert(self):
        '''Convert curb ramps GeoJSON data to DOM tree, features may be
        duplicated due to the structure of JSON.

        :return: a DOM tree structure which is equivalent to the curb ramps
                 json database.

        '''
        dom_root = etree.Element('osm')
        self.add_header(dom_root)
        id_generator = OSMIDGenerator()

        with progressbar(length=len(self.json_database['features']), label='Converting') as bar:
            for elt in self.json_database['features']:
                if elt['geometry']['type'] == 'Point':
                    osm_curbramp = etree.SubElement(dom_root, 'node')
                    self.__node_common_attribute__(osm_curbramp)
                    osm_curbramp.attrib['id'] = str(id_generator.get_next())
                    osm_curbramp.attrib['lon'] = str(elt['geometry']['coordinates'][0])
                    osm_curbramp.attrib['lat'] = str(elt['geometry']['coordinates'][1])
                    if elt['properties'] is not None:
                        for prop in elt['properties']:
                            osm_tag = etree.SubElement(osm_curbramp, 'tag')
                            osm_tag.attrib['k'] = prop
                            osm_tag.attrib['v'] = str(elt['properties'][prop]).lower()
                bar.update(1)
            bar.finish()

        return dom_root
