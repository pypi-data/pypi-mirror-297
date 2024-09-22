from setuptools import setup

setup(
    name='geobuffers',
    version='0.1',
    description='geobuffers',
    long_description='geobuffers mini package for calculating geodetic areas around points',
    author='Mikolaj Czerkawski',
    install_requires=["shapely","pyproj"]
)
