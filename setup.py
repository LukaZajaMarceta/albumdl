#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='albumdl-LukaZajaMarceta',
    version=0.1,
    packages=find_packages(),
    install_requires=['youtube_dl',
                      'html2text',
                      'python-youtube'],
    author='Luka Zaja',
    author_email='lukazajamarceta@gmail.com',
    description='Command line utility for downloading albums from youtube',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='download youtube albums timestamps comments comment description',
    url='https://github.com/LukaZajaMarceta/albumdl',
    python_requires='>=3.6',
    entry_points={"console_scripts": ['albumdl=albumdl.albumdl:main']}
)

