## Developer Note: Update Pydar's backend when new features are updated
## New offically named features: https://planetarynames.wr.usgs.gov/#nomenclature-news
import os
import pandas as pd
import pydar

if __name__ == "__main__":
	os.system('python pydar/updateCsvCORADARJPLOptions.py')
	os.system('python pydar/updateCsvSwathCoverage.py.py')
	os.system('python pydar/updateCsvFeatureNameDetails.py')

	print("New Features (diff):")
	os.system("git diff pydar/data/feature_name_details.csv | grep '^[+-][^+-]'")

	# read in all feature names from CSV
	features_df = pd.read_csv("pydar/data/feature_name_details.csv")
	features_in_csv = list(features_df["Feature Name"])

	# list of all features that exist (with both latitude/longitude values)
	retrieved_features = pydar.retrieveFeaturesFromLatitudeLongitudeRange(min_latitude=-90, max_latitude=90, min_longitude=0, max_longitude=360)

	# check if all features in CSV have both latitude/longitude values
	if not features_in_csv == retrieved_features: 
		print("\nMissing features to Fix or Ignore:")
		all_missing_features = [x for x in features_in_csv if x not in retrieved_features]
		for feature_missing in all_missing_features:
			print(feature_missing)
			feature_row = features_df[features_df["Feature Name"] ==  feature_missing]
			missing_lat_long = feature_row.columns[feature_row.isna().any()].tolist()
			print(f"\tMissing: {missing_lat_long}")
			print(f"\t{feature_row['URL'].iloc[0]}")

	print("\nAll features in CSV with latitude/longitude values")
	print("New Total Feature List to Copy in README and Test:")
	print(retrieved_features)
	print("Update README.md")
	print("Update 'feature_name_full_list' in pydar/pytests/test_error_retrieve_ids_by_time_position.py")
	print("Run: python -m pytest")
