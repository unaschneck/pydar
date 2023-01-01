# Extract flyby parameters from CASSINI

import zipfile
import os

from planetaryimage import PDS3Image
import matplotlib.pyplot as plt
from urllib import request

if __name__ == '__main__':
	flyby_num = "0065"

	label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_{0}_V03/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.LBL".format(flyby_num)
	label_name = label_url.split("/")[-1].split(".")[0] + ".txt"
	response = request.urlretrieve(label_url, label_name)
	
	data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_{0}_V03/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.ZIP".format(flyby_num)
	zipfile_name = data_url.split("/")[-1].split(".")[0] + ".zip"
	print(zipfile_name)
	response = request.urlretrieve(data_url, zipfile_name)

	with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
		zip_ref.extractall()

	from planetaryimage import PDS3Image
	zipped_image = zipfile_name.split(".")[0] + ".IMG"
	image = PDS3Image.open(zipped_image)
	fig = plt.figure(figsize=(8,8), dpi=120)
	plt.imshow(image.image, cmap='gray')
	plt.show()

	flyby_name = data_url.split("/")[-1].split(".")[0]
	os.remove("{0}.IMG".format(flyby_name))
	os.remove("{0}.txt".format(flyby_name))
	os.remove("{0}.zip".format(flyby_name))
