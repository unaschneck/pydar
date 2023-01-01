# Extract flyby parameters from CASSINI

import zipfile
import os

import pandas as pd
from planetaryimage import PDS3Image
import matplotlib.pyplot as plt
from urllib import request

def getFlybyData():
	# Header: Titan flyby id, Radar Data Take Number, Sequence number, Orbit Number/ID
	flyby_id = []
	flby_radar_take_num = []
	flyby_csv_file = os.path.join(os.path.dirname(__file__), 'data', 'cassini_flyby.csv')  # get file's directory, up one level, /data/star_data.csv
	flyby_dataframe = pd.read_csv(flyby_csv_file)
	for index, row in flyby_dataframe.iterrows():
		row = row.tolist()
		flyby_id.append(row[0])
		radar_take_num = row[1].split(" ")[1]
		while len(radar_take_num) < 4:
			radar_take_num = "0" + radar_take_num # set all radar take numbers to be four digits long: 229 -> 0229
		flby_radar_take_num.append(radar_take_num)
	# returns a list of flyby IDs and associated Radar Data Take Number
	return flyby_id, flby_radar_take_num

if __name__ == '__main__':
	avaliable_flyby_id, avaliable_observation_numbers = getFlybyData()
	flyby_observiation_num = "0065"

	if flyby_observiation_num not in avaliable_observation_numbers:
		print("Observation number '{0}' NOT FOUND in avaiable observation numbers: {1}".format(flyby_observiation_num, avaliable_observation_numbers))
		exit()
	else:
		print("Observation number '{0}' FOUND in avaiable observation numbers: {1}".format(flyby_observiation_num, avaliable_observation_numbers))

	label_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_{0}_V03/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.LBL".format(flyby_observiation_num)
	label_name = label_url.split("/")[-1].split(".")[0] + ".txt"
	response = request.urlretrieve(label_url, label_name)
	
	data_url = "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_{0}_V03/DATA/BIDR/BIBQD05S184_D065_T008S03_V03.ZIP".format(flyby_observiation_num)
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
