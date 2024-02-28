from MapCreator import (
    match_buildings_to_parcels,
    read_geospatial_metadata_from_tif,
    create_detection_shapefile,
)
from ResultCreator import create_results_pdf, annotate_tracking_results
from YoloTracker import detect_objects_in_image
from FilesPreprocessor import (
    archive_and_delete_files,
    generate_unique_name,
    convert_tif_to_jpg,
    convert_tif_to_jpg,
)
import cv2 as cv


def analyze_tif(
    path_to_tif,
    path_to_save_folder,
    path_to_output_zip_folder,
    path_to_model,
    path_to_land_map,
):
    unique_name = generate_unique_name(path_to_tif)
    base_shapefile_path = path_to_save_folder + unique_name + ".shp"
    output_boxed_jpg_path = path_to_save_folder + unique_name + "_boxed.jpg"
    output_shapefile_path = path_to_save_folder + unique_name + "_with_parcel.shp"
    output_pdf_path = path_to_save_folder + unique_name + ".pdf"
    output_zip_path = path_to_output_zip_folder, +unique_name + "_archive.zip"

    transform, coordinates = read_geospatial_metadata_from_tif(path_to_tif)

    img = convert_tif_to_jpg(path_to_tif)

    track_results, names = detect_objects_in_image(img, path_to_model)
    
    annotated_img = annotate_tracking_results(img, track_results, names)
    cv.imwrite(output_boxed_jpg_path, annotated_img)
    
    create_detection_shapefile(
        base_shapefile_path,
        track_results,
        names,
        transform,
        coordinates,
    )


    report = match_buildings_to_parcels(
        base_shapefile_path, output_shapefile_path, path_to_land_map
    )

    create_results_pdf(report, output_pdf_path)

    path_to_zip = archive_and_delete_files(
        unique_name, path_to_save_folder, output_zip_path
    )

    return path_to_zip


def analyze_photo(
    img,
    path_to_save_folder,
    path_to_model,
    path_to_land_map,
    transform,
    coordinates,
):  # TODO
    unique_name = "file"
    base_shapefile_path = path_to_save_folder + unique_name + ".shp"
    output_shapefile_path = path_to_save_folder + unique_name + "_with_parcel.shp"

    track_results, names = detect_objects_in_image(img, path_to_model)

    annotated_img = annotate_tracking_results(img, track_results, names)

    create_detection_shapefile(
        base_shapefile_path,
        track_results,
        names,
        transform,
        coordinates,
    )

    report = match_buildings_to_parcels(
        base_shapefile_path, output_shapefile_path, path_to_land_map
    )
    return annotated_img, report
