from json import load as load_json
import click
from osmizer.features.crossing import Crossing
from osmizer.features.curbramp import CurbRamp
from osmizer.features.feature import Feature
from osmizer.features.sidewalk import Sidewalk


def validation_success():
    '''
    Operations to be done when validation success

    :return: None
    '''
    click.echo('Checked: Valid GeoJSON Input File')
    click.echo('...')


def validation_failure():
    '''
    Operations to be done when validation fails

    :return: None
    '''
    click.echo('ERROR: Non-Valid GeoJSON Input File')
    click.echo('...')


def operation_finish():
    '''
    Operations to be done after all operations are performed successfully

    :return: None
    '''
    click.echo('Operation Finished')
    click.echo('...')


def build_features(feature_type, file_in):
    '''
    Build a feature object

    :param feature_type: type of the feature to be built
    :param file_in: the input data base
    :return: the feature object containing the input data base
    '''
    features = None
    features_json = load_json(open(file_in))

    if feature_type == 'sidewalks':
        features = Sidewalk(features_json)
    if feature_type == 'curbramps':
        features = CurbRamp(features_json)
    if feature_type == 'crossings':
        features = Crossing(features_json)
    return features


@click.group(invoke_without_command=False)
def cli():
    pass


@cli.command()
@click.argument('json_type')
@click.argument('file_in', type=click.Path(exists=True, readable=True,
                allow_dash=True))
def validate(json_type, file_in):
    features = build_features(json_type, file_in)

    if features is None:
        click.echo('Invalid JSON input type')
        return

    if features.validate():
        validation_success()
    else:
        validation_failure()

    operation_finish()


@cli.command()
@click.option('--tolerance', default=0.0000001,
              help=('Tolerance when deciding if two close points should be \
                     merged'))
@click.argument('json_type')
@click.argument('file_in', type=click.Path(exists=True, readable=True,
                allow_dash=True))
@click.argument('file_out', type=click.Path(exists=False, writable=True,
                allow_dash=True))
def convert(json_type, file_in, file_out, tolerance):
    features = build_features(json_type, file_in)

    if features is None:
        click.echo('Invalid JSON input type')
        return

    xml_dom = features.convert()
    if xml_dom is False:
        click.echo('Failed to Read Input File')
        click.echo('Operation Terminated')
        return
    else:
        click.echo('Input File Read Successfully')
        click.echo('...')

    click.echo('Running Deduplicate(Tolerance: %.8f)' % tolerance)
    features.dedup(xml_dom, tolerance)
    click.echo('...')

    click.echo('Saving file to %s' % file_out)
    if features.to_xml(xml_dom, file_out):
        click.echo('OSM file saved: %s' % file_out)
        click.echo('...')
    else:
        click.echo('OSM file failed to save')
        click.echo('Operation Terminated')
        return

    operation_finish()


@cli.command()
@click.argument('file_in', type=click.Path(exists=True, readable=True,
                allow_dash=True), nargs=-1)
@click.argument('file_out', type=click.Path(exists=False, writable=True,
                allow_dash=True), nargs=1)
def merge(file_in, file_out):
    xml_merged = Feature.merge(file_in)
    click.echo('...')
    if xml_merged is None:
        click.echo('Operation Terminated')
        click.echo('...')
        return
    Feature.to_xml(xml_merged, file_out)
    operation_finish()


if __name__ == '__main__':
    cli()
