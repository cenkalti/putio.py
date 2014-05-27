# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='putio.py',
    version='2.3.1',
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    url='http://github.com/cenkalti/putio.py',
    py_modules=['putio'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['requests', 'iso8601'],
)
