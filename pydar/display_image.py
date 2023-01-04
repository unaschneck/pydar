## Display Image
import logging
import os

from planetaryimage import PDS3Image
import matplotlib.pyplot as plt

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def displayImages(image_directory):
	# Display all images in the image directory specified
	for filename in os.listdir(image_directory):
		if 'IMG' in filename:
			image_file = os.path.join("{0}/{1}".format(image_directory, filename))
			logger.info("Displaying Image: {0}".format(image_file))
			image = PDS3Image.open(image_file)
			fig = plt.figure(figsize=(4,6), dpi=120)
			plt.title(filename)
			plt.xlabel("Pixels #")
			plt.ylabel("Pixels #")
			plt.imshow(image.image, cmap='gray')
	plt.show()
