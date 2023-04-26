# Pytest for display_image.py
# pydar/pydar/: pytest -vs --disable-pytest-warnings --show-capture=no --capture=sys -vv
import logging

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
def test_displayImages_imageDirectoryRequired(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [image_directory]: image_directory is required"

@pytest.mark.parametrize("image_directory_invalid, image_directory_error_output", invalid_non_str_options)
def test_displayImages_ImageDirectoryInvalidTypes(caplog, image_directory_invalid, image_directory_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory=image_directory_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [image_directory]: Must be a str, current type = '{0}'".format(image_directory_error_output)

@pytest.mark.parametrize("fig_title_invalid, fig_title_error_output", invalid_non_str_options)
def test_displayImages_figureTitleInvalidTypes(caplog, fig_title_invalid, fig_title_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", fig_title=fig_title_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [fig_title]: Must be a str, current type = '{0}'".format(fig_title_error_output)

@pytest.mark.parametrize("fig_title_invalid, fig_title_error_output", invalid_non_str_options)
def test_displayImages_figureTitleInvalidTypes(caplog, fig_title_invalid, fig_title_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", fig_title=fig_title_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [fig_title]: Must be a str, current type = '{0}'".format(fig_title_error_output)

@pytest.mark.parametrize("cmap_invalid, cmap_error_output", invalid_non_str_options)
def test_displayImages_cmapInvalidTypes(caplog, cmap_invalid, cmap_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", cmap=cmap_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [cmap]: Must be a str, current type = '{0}'".format(cmap_error_output)

@pytest.mark.parametrize("figsize_n_invalid, figsize_n_error_output", invalid_non_int_options)
def test_displayImages_figureSizeInvalidTypes(caplog, figsize_n_invalid, figsize_n_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", figsize_n=figsize_n_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [figsize_n]: Must be a int, current type = '{0}'".format(figsize_n_error_output)

@pytest.mark.parametrize("fig_dpi_invalid, fig_dpi_error_output", invalid_non_int_options)
def test_displayImages_figureDPIInvalidTypes(caplog, fig_dpi_invalid, fig_dpi_error_output):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", fig_dpi=fig_dpi_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [fig_dpi]: Must be a int, current type = '{0}'".format(fig_dpi_error_output)

def test_displayImages_figureSizeInvalidRange(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", figsize_n=0)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [figsize_n]: figsize_n must be greater than 1, current value = '0'"

def test_displayImages_figureDPIInvalidRange(caplog):
	# Test:
	with pytest.raises(SystemExit):
		pydar.displayImages(image_directory="pydar_results/testing", fig_dpi=0)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [fig_dpi]: fig_dpi must be greater than 1, current value = '0'"

## displayImages() #####################################################
