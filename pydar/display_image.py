#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      display_image.py displays the PDR images in CORADR files                                   #
#          for flyby observations and IDs                                                         #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - display_all_images: displays all the images             #
#                                              from the flyby results in Matplotlib               #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
import logging
import os

# Related Third Party Imports
import rasterio
import matplotlib.pyplot as plt

# Internal Local Imports
import pydar

########################################################################

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


#### DISPLAY ALL PDR IMAGES IN A DIRECTORY #############################
def display_all_images(image_directory: str = None,
                       fig_title: str = None,
                       cmap: str = "gray",
                       figsize_n: int = 6,
                       fig_dpi: int = 120) -> None:
    # Display all images in the image directory specified
    #   plt.show() all imgs in a given directory

    pydar._error_handling_display_all_images(image_directory=image_directory,
                                             fig_title=fig_title,
                                             cmap=cmap,
                                             figsize_n=figsize_n,
                                             fig_dpi=fig_dpi)

    # Display all IMG files in directory
    for filename in os.listdir(image_directory):
        if 'LBL' in filename:
            image_file = os.path.join(f"{image_directory}/{filename}")

            logger.info(f"Displaying Image: {image_file}")
            image = rasterio.open(image_file).read()
            image = image[0, :, :]

            fig = plt.figure(figsize=(figsize_n, figsize_n), dpi=fig_dpi)
            if fig_title is None:
                plt.title(filename)
            else:
                plt.title(fig_title)
            plt.xlabel("Pixels #")
            plt.ylabel("Pixels #")
            plt.imshow(image, cmap=cmap)
            plt.show()

    # Log error to user if no image files given
    if not any(".LBL" in sub for sub in os.listdir(image_directory)
               ):  # if directory files does not contain any .IMG files
        logger.info(
            f"\nINFO: Unable to display images, {image_directory} does not contain an LBL file\n"
        )
    if not any(".IMG" in sub for sub in os.listdir(image_directory)
               ):  # if directory files does not contain any .IMG files
        logger.info(
            f"\nINFO: Unable to display images, {image_directory} does not contain an IMG file\n"
        )
