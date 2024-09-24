# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libtokit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libtokit',
    'version': '0.1.2',
    'description': 'A simple utility for creating directories.',
    'long_description': 'None',
    'author': 'pytools',
    'author_email': 'hyhlinux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
