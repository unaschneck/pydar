# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION="0.0.1"
DESCRIPTION="A Python package for Access and manipulation of Cassini RADAR images"

with open("README.md", "r") as f:
	long_description_readme = f.read()

setup(
	name="pydar",
	version=VERSION,
	description=DESCRIPTION,
	long_description=long_description_readme,
	long_description_content_type='text/markdown',
	url="https://github.com/unaschneck/pydar",
	download_url="https://github.com/unaschneck/pydar/archive/refs/tags/v{0}.tar.gz".format(VERSION),
	author="",
	keywords=[],
	license="",
	classifiers=[],
	packages=find_namespace_packages(include=['pydar', 'pydar.*']),
	include_package_data=True,
	install_requires=[],
	python_requires='>=3.7'
)
