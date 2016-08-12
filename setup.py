'''osmizer: convert simple GeoJSON-schema feature layers to the OSM XML format.

Documentation available at https://github.com/OpenSidewalks/osmizer.
'''

import re
import sys

from setuptools import setup, find_packages

# Check python versions
if sys.version_info.major < 3:
    print('osmizer is currently compatible only with Python 3.')
    sys.exit(1)

# Get version from package __init__.py
with open('osmizer/__init__.py', 'r') as f:
    __version__ = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            f.read(), re.MULTILINE).group(1)
if not __version__:
    raise RuntimeError('Cannot find version information')

doclines = __doc__.split('\n')

config = {
    'name': 'osmizer',
    'version': __version__,
    'description': doclines[0],
    'long_description': '\n'.join(doclines[2:]),
    'author': '',
    'author_email': '',
    'maintainer': '',
    'maintainer_email': '',
    'url': 'https://github.com/OpenSidewalks/osmizer',
    'license': 'BSD',
    'download_url': 'https://github.com/OpenSidewalks/osmizer.git',
    'install_requires': ['click',
                         'jsonschema',
                         'lxml',
                         'rtree'],
    'packages': find_packages(),
    'include_package_data': True,
    'classifiers': ['Programming Language :: Python',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3 :: Only'],
    'zip_safe': False,
    'entry_points': '''
        [console_scripts]
        osmizer=osmizer.__main__:cli
    '''
}

setup(test_suite='nose.collector',
      **config)
