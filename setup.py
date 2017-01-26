# coding=utf-8
import re
from setuptools import setup

with open('putiopy.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

setup(
    name='putio.py',
    description='Python client for put.io API v2',
    version=version,
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    url='https://github.com/cenk/putio.py',
    py_modules=['putiopy'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=['requests', 'tus.py'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
