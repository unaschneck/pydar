# Test Expected Error Messages from display_image.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_error_display_image.py -xv

# Standard Library Imports
import re

# Related Third Party Imports
import pytest

# Internal Local Imports
import pydar

invalid_non_str_options = [(1961, "<class 'int'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]

invalid_non_int_options = [("1961", "<class 'str'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]


## display_all_images() #####################################################
def test_displayAllImages_imageDirectoryRequired():
    with pytest.raises(
            ValueError,
            match=re.escape("[image_directory]: image_directory is required")):
        pydar.display_all_images(image_directory=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_displayAllImages_ImageDirectoryInvalidTypes(invalid_input,
                                                     error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[image_directory]: Must be a str, current type = '{error_output}'"
            )):
        pydar.display_all_images(image_directory=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_displayAllImages_figureTitleInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[fig_title]: Must be a str, current type = '{error_output}'")
    ):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 fig_title=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_displayAllImages_cmapInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[cmap]: Must be a str, current type = '{error_output}'")):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 cmap=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_int_options)
def test_displayAllImages_figureSizeInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[figsize_n]: Must be a int, current type = '{error_output}'")
    ):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 figsize_n=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_int_options)
def test_displayAllImages_figureDPIInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[fig_dpi]: Must be a int, current type = '{error_output}'")):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 fig_dpi=invalid_input)


def test_displayAllImages_figureSizeInvalidRange():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[figsize_n]: figsize_n must be greater than 1, current value = '0'"
            )):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 figsize_n=0)


def test_displayAllImages_figureDPIInvalidRange():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[fig_dpi]: fig_dpi must be greater than 1, current value = '0'"
            )):
        pydar.display_all_images(image_directory="pydar_results/testing",
                                 fig_dpi=0)


## display_all_images() #####################################################
