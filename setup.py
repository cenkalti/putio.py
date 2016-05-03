# coding=utf-8
from setuptools import setup

setup(
    name='putio.py',
    version='2.4.4',
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    url='http://github.com/cenkalti/putio.py',
    py_modules=['putio'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=['requests'],
)
