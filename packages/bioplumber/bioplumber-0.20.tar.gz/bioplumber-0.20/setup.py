# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioplumber']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bioplumber',
    'version': '0.20',
    'description': '',
    'long_description': None,
    'author': 'ParsaGhadermazi',
    'author_email': '54489047+ParsaGhadermazi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
