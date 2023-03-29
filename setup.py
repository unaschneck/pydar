# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION="1.0.0"
DESCRIPTION="A Python package to access, download, view, and manipulate Cassini RADAR images"

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
	author="Una Schneck (unaschneck), Cora Schneck (cyschneck)",
	keywords=[],
	license="MIT",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.7",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Physics",
		"Topic :: Scientific/Engineering :: Image Processing",
		"Topic :: Scientific/Engineering :: Visualization",
		"Topic :: Scientific/Engineering :: Astronomy"
	],
	packages=find_namespace_packages(include=['pydar', 'pydar.*']),
	include_package_data=True,
	install_requires=[
			"beautifulsoup4>=4.11.1",
			"matplotlib>=3.1.0",
			"pandas>=1.5.2",
			"pdr>=0.7.3",
			"planetaryimage>=0.5.0",
			"pyproj>=3.4.1",
			"pytest>=7.2.2",
			"urllib3>=1.26.9"
			],
	python_requires='>=3.9'
)
