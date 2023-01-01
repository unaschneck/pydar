# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION="0.0.2"
DESCRIPTION="A Python package for access and manipulation of Cassini RADAR images"

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
	author=["Una Schneck (unaschneck)","C. Y. Schneck (cyschneck)"],
	keywords=[],
	license="MIT",
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.7",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Physics",
		"Topic :: Scientific/Engineering :: Visualization",
		"Topic :: Scientific/Engineering :: Astronomy"
	],
	packages=find_namespace_packages(include=['pydar', 'pydar.*']),
	include_package_data=True,
	install_requires=[],
	python_requires='>=3.7'
)
