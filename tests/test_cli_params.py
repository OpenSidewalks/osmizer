import click
from click.testing import CliRunner
import osmizer.__main__ as osmizer


runner = CliRunner()


def test_invalid_option():
    try:
        @click.command()
        @click.option('foo')
        def cli(foo):
            pass
    except TypeError as e:
        assert 'No options defined but a name was passed (foo).' \
            in str(e)
    else:
        assert False, 'Expected a type error because of an invalid option.'


def test_help_text():
    '''Tests appropriate running and output text with help parameter.'''
    result = runner.invoke(osmizer.cli, ['--help'])
    assert result.exit_code == 0


def test_cli_params():
    test_invalid_option()
    test_help_text()


if __name__ == '__main__':
    runner = CliRunner()
    test_cli_params()
