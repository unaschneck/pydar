import pydar

if __name__ == '__main__':
	pydar.extractFlybyDataImages(flyby_observation_num='65',
								resolution='D',
								segment_num="S01")
	pydar.displayImages("results/CORADR_0065_V03_S01") # display image for user verification

