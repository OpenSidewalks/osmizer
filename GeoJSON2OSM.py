import click
from Libraries import Sidewalk


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

    input_json = open(file_in)
    sidewalk = Sidewalk.Sidewalk(input_json)

    if validate:
        if sidewalk.validate():
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

    xml_dom = sidewalk.convert()
    if xml_dom is False:
        click.echo('Failed to Read Input File')
        click.echo('Operation Terminated')
        return
    else:
        click.echo('Input File Read Successfully')
        click.echo('...')

    if 0.00001 < tolerance < 1:
        click.echo('Merging(Tolerance: %.4f)' % tolerance)
        sidewalk.dedup(xml_dom, tolerance)
        click.echo('...')

    if sidewalk.to_xml(xml_dom, file_out):
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
