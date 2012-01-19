from setuptools import setup

setup(
    name='Putio-API-v2',
    version='1.0',
    long_description=__doc__,
    packages=['putio2'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'iso8601'],
    entry_points = {
        'console_scripts': [
            'putio-cli = cli:main',
            ],
        }
)
