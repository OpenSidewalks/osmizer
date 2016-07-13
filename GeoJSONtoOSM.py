import geopandas as gpd
import click


def read_input(file_path):
    try:
        file_read = gpd.read_file(file_path, mode='r', driver='GeoJSON')
    except:
        return -1
    return file_read


def validate_input(gpd_database):
    # TODO: Validate Input
    return True


def to_OSM(gpd_database, output_path):
    # TODO: Output file to OSM format
    return True


@click.command()
@click.option('--validate/--no-validate', default=True, help='Validate the input GeoJSON file before conversion')
@click.argument('file_in', type=click.Path(exists=True, readable=True, allow_dash=True))
@click.argument('file_out', type=click.Path(exists=False, writable=True, allow_dash=True))
def converter(file_in, file_out, validate):
    click.echo('File in: ' + file_in)
    click.echo('File out: ' + file_out)

    database = read_input(file_in)
    if database == -1:
        click.echo('Failed to Read Input File')
        return
    else:
        click.echo('Input File Read Successfully')

    if validate:
        if validate_input(database):
            click.echo('Checked: Valid Input File')
        else:
            click.echo('Checked: Non-Valid Input File')
            click.echo('Operation Terminated')
            return

    if to_OSM(database, file_out):
        click.echo('OSM file saved')
    else:
        click.echo('OSM file failed to save')
        click.echo('Operation Terminated')
        return

    click.echo('Operation Complete')


if __name__ == '__main__':
    converter()
