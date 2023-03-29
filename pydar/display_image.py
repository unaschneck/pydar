## Display PDR images in Matplotlib

# Built in Python functions
import logging
import os

# External Python libraries (installed via pip install)
from planetaryimage import PDS3Image
import matplotlib.pyplot as plt

# Internal Pydar reference to access functions, global variables, and error handling
import pydar

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

#### DISPLAY ALL PDR IMAGES IN A DIRECTORY #############################
def displayImages(image_directory=None, fig_title=None, figsize_n=6, fig_dpi=120):
	# Display all images in the image directory specified
	#	plt.show() all imgs in a given directory

	pydar.errorHandlingDisplayImages(image_directory=image_directory,
									fig_title=fig_title,
									figsize_n=figsize_n,
									fig_dpi=fig_dpi)

	# Display all IMG files in directory
	for filename in os.listdir(image_directory):
		if 'IMG' in filename:
			image_file = os.path.join("{0}/{1}".format(image_directory, filename))

			logger.info("Displaying Image: {0}".format(image_file))

			image = PDS3Image.open(image_file)
			logger.debug("Displaying Dimensions: {0}".format(image.shape))

			fig = plt.figure(figsize=(figsize_n,figsize_n), dpi=fig_dpi)
			if fig_title is None:
				plt.title(filename)
			else:
				plt.title(fig_title)
			plt.xlabel("Pixels #")
			plt.ylabel("Pixels #")
			plt.imshow(image.image, cmap='gray')
			plt.show()

	# Log error to user if no image files given
	if not any(".IMG" in sub for sub in os.listdir(image_directory)): # if directory files does not contain any .IMG files
		logger.info("\nINFO: Unable to display images, {0} does not contain an IMG file\n".format(image_directory))
