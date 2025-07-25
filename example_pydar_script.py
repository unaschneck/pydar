import pydar

if __name__ == '__main__':
	season = pydar.titan_season(year="2025", month="04", day="14", hemisphere="south")
	print(season)
	'''
    # VERSION 1:
    ## Get swatch coverage based on latitude/longitude, Time, or Feature
    feature_name = "Ontario Lacus"
    flyby_ids_name = pydar.ids_from_feature_name(feature_name=feature_name)
    print(
        f"Flyby IDS based on Feature Name '{feature_name.title()}' = {flyby_ids_name}"
    )

    flyby_ids_with_segments = pydar.ids_from_latlon(latitude=-80,
                                                    longitude=170)
    print(
        f"\nFlyby IDS based on Latitude/Longitude = {flyby_ids_with_segments}")

    flyby_ids_range = pydar.ids_from_latlon_range(min_latitude=-82,
                                                  max_latitude=-72,
                                                  min_longitude=183,
                                                  max_longitude=185)
    print(f"\nFlyby IDS based on Latitude/Longitude Range = {flyby_ids_range}")

    feature_names_list = pydar.features_from_latlon(latitude=-72,
                                                    longitude=183)
    print(
        f"\nFeature Names Found at -72 latitude and 183 longitude = {feature_names_list}"
    )

    feature_names_list = pydar.features_from_latlon_range(min_latitude=-82,
                                                          max_latitude=-72,
                                                          min_longitude=183,
                                                          max_longitude=190)
    print(
        f"\nFeature Names Found in Latitude/Longitude Range = {feature_names_list}"
    )

    flyby_ids_time = pydar.ids_from_time(year=2005, doy=301)
    print(f"\nFlyby IDS based on a specific timestamp = {flyby_ids_time}")

    flyby_ids_time_range = pydar.ids_from_time_range(start_year=2004,
                                                     start_doy=299,
                                                     start_hour=2,
                                                     start_minute=15,
                                                     start_second=23,
                                                     start_millisecond=987,
                                                     end_year=2005,
                                                     end_doy=301,
                                                     end_hour=2,
                                                     end_minute=15,
                                                     end_second=23,
                                                     end_millisecond=987)
    print(
        f"\nFlyby IDS based on a range of timestamps = {flyby_ids_time_range}")

    # Convert Flby Id into an Observation Number
    flyby_id_value = "T65"
    observation_num = pydar.id_to_observation(flyby_id=flyby_id_value)
    print(
        f"\nFlyby ID '{flyby_id_value}' is observation number = {observation_num}"
    )

    observation_num = "211"
    flyby_id = pydar.observation_to_id(flyby_observation_num=observation_num)
    print(f"\nObservation Number '{observation_num}' is flyby id = {flyby_id}")

    # Extract Flyby Data Files to results/ directory
    pydar.extract_flyby_images(flyby_id="T65",
                               flyby_observation_num=None,
                               resolution='D',
                               segment_num="S01")

    # Display all Images in pydar_results/ directory
    pydar.display_all_images("pydar_results/CORADR_0211_V03_S01")

    # Read AAREADME to console
    pydar.aareadme_options()
    pydar.read_aareadme(
        coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
        section_to_print="INSTRUMENT_name")

    # Read .LBL to console
    #pydar.lbl_options()
    #pydar.read_lbl_readme(
    #    coradr_results_directory="pydar_results/CORADR_0211_V03_S01/",
    #    section_to_print="LOOK_DIrecTION")

    # VERSION 2: (Upcoming)
    #pydar.extractMetadata()

    # SBDR Shapefile
    #pydar.sbdrMakeShapeFile(filename="pydar/testing_files/SBDR_15_D065_V03.TAB",
    #                       saronly=3,
    #                       usepassive=False,
    #                       lon360=True)
	'''
