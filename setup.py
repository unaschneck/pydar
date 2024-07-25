# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION="1.3.3"
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
	download_url=f"https://github.com/unaschneck/pydar/archive/refs/tags/v{VERSION}.tar.gz",
	author="Una Schneck (unaschneck), Cora Schneck (cyschneck)",
	keywords=["geophysics", "python", "astronomy", "nasa", "radar", "planetary-science", "cassini", "jpl"],
	license="MIT",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Physics",
		"Topic :: Scientific/Engineering :: Image Processing",
		"Topic :: Scientific/Engineering :: Visualization",
		"Topic :: Scientific/Engineering :: Astronomy"
	],
	packages=find_namespace_packages(include=['pydar', 'pydar.*'],
        exclude=['pydar.pytests']),
	include_package_data=True,
	install_requires=[
			"beautifulsoup4",
			"matplotlib",
			"pandas",
			"pdr",
			"pyproj",
			"pytest",
			"rasterio",
			"urllib3"
			],
	python_requires='>=3.10'
)
