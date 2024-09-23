# VineyardUtils
A Python package for digital agriculture in vineyard-related activities

VineyardUtils is a Python package designed to assist in handling georeferenced data, processing KML files, and organizing data from field activities in vineyards. This package provides several utility functions and tools to streamline data operations and analysis, plus aims to process data without directly involving packages like (gdal and rasterio) into python environments.

# Installation

You can install VineyardUtils using pip:

pip install VineyardUtils

Note: for some functions an external OSGeo package must be installed in the system. 

# Usage

import VineyardUtils

# Functions

Datasampler

    cut_data(dataframe, time, timecolumn):
    Splits a DataFrame based on time intervals specified.

    field_counter(dataf, min_number, exclude_words=None):
    Counts occurrences of fields in a DataFrame and appends the most common field as a new column.

    get_summary_stats(df, columns=None):
    Computes summary statistics from specified columns in a DataFrame.

Elevation

    get_elevation(osgeopath, coordmode, geotiff_filename, lat, lon):
    Retrieves elevation data from a GeoTIFF file using gdallocationinfo. Make sure that Osgeo4w is installed first since path to its folder is required. 

    crop_geotiff(osgeopath, srsmode, minlon, minlat, maxlon, maxlat, source_path_tif, output_path_tif):
    Crops a GeoTIFF file to specified bounding box coordinates.

    get_elevation_list(osgeopath, sourcename, coordmode, geotiff_filename):
    Retrieves a list of elevations from a list of coordinates stored in a file.

    add_elevation_to_df(df, latcolname, loncolname, osgeopath, coordmode, geotiff_filename, crop=True/False, type_srs="EPSG:4326"):
    Adds elevation data to a DataFrame based on latitude and longitude columns. Type_srs variable is optional ("EPSG:4326" is indeed set by default.
    
    Example: 
    new_df = elevation.add_elevation_to_df(df, "Latitude", "Longitude",'C:\\OSGeo4W\\OSGeo4W.bat', '-wgs84', 'C:\\OSGeo4W\eumapdem.tif', crop=1)
    
    Note that by setting crop=1 the algorithm will cut the geotiff along the minimum and maximum lat/lon coordinates in the dataframe. It may take longer, but it is faster for big dataframes. 

KMLUtils

    extract_coordinates(file_path):
    Extracts longitude and latitude coordinates from a KML file.

    calculate_angle(x1, y1, x2, y2, x3, y3):
    Calculates the angle between three points.

    iterate_check_angle(longitudes, latitudes, tanklevels, min_angle, max_angle, elevation):
    Iterates through a list of coordinates to find tuples based on specified angles.

    generate_alpha_shapes(dataframe, alpha=0.2):
    Generates alpha shapes from longitude and latitude coordinates.

    create_kml(dataframe, row_tuples, kml_filename='outputfile.kml'):
    Creates a KML file with polygons and lines based on specified rows of coordinates.

# Dependencies

    pandas
    numpy
    scikit-learn
    simplekml
    alphashape

# Contributing

Contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License

This project is licensed under the MIT License - see the LICENSE file for details.