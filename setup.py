# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='putio.py',
    version='1.0',
    author=u'Cenk Altı',
    url='http://github.com/cenkalti/putio.py',
    # packages=['putio2'],
    py_modules=['putio'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['requests', 'iso8601'],
)
