## Logging set up for .INFO
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def testing():
	print(__name__)
	logger.critical("hello Titan")
	exit()

