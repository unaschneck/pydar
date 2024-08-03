import pydar

if __name__ == '__main__':
    # VERSION 1:
    ## Get swatch coverage based on latitude/longitude, Time, or Feature
    feature_name = "Ontario Lacus"
    flyby_ids_name = pydar.retrieveIDSByFeatureName(feature_name=feature_name)
    print("Flyby IDS based on Feature Name '{0}' = {1}".format(
        feature_name.title(), flyby_ids_name))

    flyby_ids_with_segments = pydar.retrieveIDSByLatitudeLongitude(
        latitude=-80, longitude=170)
    print("\nFlyby IDS based on Latitude/Longitude = {0}".format(
        flyby_ids_with_segments))

    flyby_ids_range = pydar.retrieveIDSByLatitudeLongitudeRange(
        min_latitude=-82,
        max_latitude=-72,
        min_longitude=183,
        max_longitude=185)
    print("\nFlyby IDS based on Latitude/Longitude Range = {0}".format(
        flyby_ids_range))

    feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitude(
        latitude=-72, longitude=183)
    print(
        "\nFeature Names Found at -72 latitude and 183 longitude = {0}".format(
            feature_names_list))

    feature_names_list = pydar.retrieveFeaturesFromLatitudeLongitudeRange(
        min_latitude=-82,
        max_latitude=-72,
        min_longitude=183,
        max_longitude=190)
    print("\nFeature Names Found in Latitude/Longitude Range = {0}".format(
        feature_names_list))

    flyby_ids_time = pydar.retrieveIDSByTime(year=2005, doy=301)
    print("\nFlyby IDS based on a specific timestamp = {0}".format(
        flyby_ids_time))

    flyby_ids_time_range = pydar.retrieveIDSByTimeRange(start_year=2004,
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
    print("\nFlyby IDS based on a range of timestamps = {0}".format(
        flyby_ids_time_range))

    # Convert Flby Id into an Observation Number
    flyby_id_value = "T65"
    observation_num = pydar.convertFlybyIDToObservationNumber(
        flyby_id=flyby_id_value)
    print("\nFlyby ID '{0}' is observation number = {1}".format(
        flyby_id_value, observation_num))

    observation_num = "211"
    flyby_id = pydar.convertObservationNumberToFlybyID(
        flyby_observation_num=observation_num)
    print("\nObservation Number '{0}' is flyby id = {1}".format(
        observation_num, flyby_id))

    # Extract Flyby Data Files to results/ directory
    pydar.extractFlybyDataImages(flyby_id="T65",
                                 flyby_observation_num=None,
                                 resolution='D',
                                 segment_num="S01")

    # Display all Images in pydar_results/ directory
    pydar.displayImages(image_directory="pydar_results/CORADR_0211_V03_S01")

    # Read AAREADME to console
    pydar.returnAAREADMEOptions()
    pydar.readAAREADME(
        coradr_results_directory="pydar_results/CORADR_0211_V03_S01",
        section_to_print="INSTRUMENT_name")

    # Read .LBL to console
    pydar.returnLBLOptions()
    pydar.readLBLREADME(
        coradr_results_directory="pydar_results/CORADR_0211_V03_S01/",
        section_to_print="LOOK_DIrecTION")

    # VERSION 2: (Upcoming)
    #pydar.extractMetadata()

    # SBDR Shapefile
    #pydar.sbdrMakeShapeFile(filename="pydar/testing_files/SBDR_15_D065_V03.TAB",
    #                       saronly=3,
    #                       usepassive=False,
    #                       lon360=True)
