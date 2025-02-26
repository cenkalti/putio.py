# coding=utf-8
import os

from setuptools import setup


def read(*fname):
    with open(os.path.join(os.path.dirname(__file__), *fname)) as f:
        return f.read()


try:
    version = read("VERSION").strip()
except FileNotFoundError:
    version = "0"

setup(
    name="putio.py",
    description="Python client for put.io API v2",
    version=version,
    author="Cenk Altı",
    author_email="cenkalti@gmail.com",
    url="https://github.com/cenkalti/putio.py",
    py_modules=["putiopy"],
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=["requests", "tus.py", "six"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
    ],
)
