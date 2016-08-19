import cProfile
from json import load as load_json

from osmizer.features.sidewalk import Sidewalk


def build_features(feature_type, file_in):
    '''
    Build a feature object

    :param feature_type: type of the feature to be built
    :param file_in: the input data base
    :return: the feature object containing the input data base
    '''
    features_json = load_json(open(file_in))
    features = Sidewalk(features_json)

    return features


def convert(json_type, file_in):
    features = build_features(json_type, file_in)

    if features is None:
        print('Invalid JSON input type')
        return

    xml_dom = features.convert()
    if xml_dom is False:
        print('Failed to Read Input File')
        print('Operation Terminated')
        return
    else:
        print('Input File Read Successfully')
        print('...')

    return features, xml_dom


def dedupe(features, xml_dom, tolerance=0.00001):
    features.dedup(xml_dom, tolerance)


for i, geojson in enumerate(['sidewalks-v1.geojson', 'sidewalks-v2.geojson',
                             'sidewalks-v3.geojson']):
    print()
    print('----------------------------------------------')
    print('Deduping v{}'.format(i + 1))
    features, xml_dom = convert('sidewalks', geojson)
    cProfile.run('dedupe(features, xml_dom)')
    print('----------------------------------------------')
    print()
