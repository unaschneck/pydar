# Pytest for display_image.py
# pydar/pydar/: pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys -vv
import re

# External Python libraries (installed via pip install)
import pytest

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]


invalid_non_int_options = [("1961", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

## displayImages() #####################################################
def test_displayImages_imageDirectoryRequired():
	with pytest.raises(ValueError, match=re.escape("[image_directory]: image_directory is required")):
		pydar.displayImages(image_directory=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_displayImages_ImageDirectoryInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[image_directory]: Must be a str, current type = '{error_output}'")):
		pydar.displayImages(image_directory=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_displayImages_figureTitleInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[fig_title]: Must be a str, current type = '{error_output}'")):
		pydar.displayImages(image_directory="pydar_results/testing", fig_title=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_displayImages_cmapInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[cmap]: Must be a str, current type = '{error_output}'")):
		pydar.displayImages(image_directory="pydar_results/testing", cmap=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_displayImages_figureSizeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[figsize_n]: Must be a int, current type = '{error_output}'")):
		pydar.displayImages(image_directory="pydar_results/testing", figsize_n=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_displayImages_figureDPIInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[fig_dpi]: Must be a int, current type = '{error_output}'")):
		pydar.displayImages(image_directory="pydar_results/testing", fig_dpi=invalid_input)

def test_displayImages_figureSizeInvalidRange():
	with pytest.raises(ValueError, match=re.escape("[figsize_n]: figsize_n must be greater than 1, current value = '0'")):
		pydar.displayImages(image_directory="pydar_results/testing", figsize_n=0)

def test_displayImages_figureDPIInvalidRange():
	with pytest.raises(ValueError, match=re.escape("[fig_dpi]: fig_dpi must be greater than 1, current value = '0'")):
		pydar.displayImages(image_directory="pydar_results/testing", fig_dpi=0)

## displayImages() #####################################################
