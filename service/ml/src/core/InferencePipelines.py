from MapCreator import (
    process_detection_results,
    read_geospatial_metadata_from_tif,
    create_buildings_shapefile,
)
from ResultCreator import create_result_csv, annotate_tracking_results
from YoloTracker import detect_objects_in_image
from FilesPreprocessor import (
    archive_and_delete_files,
    generate_unique_name,
    convert_image,
)
import cv2 as cv
import time


def analyze_tif(
    path_to_tif: str,
    path_to_save_folder: str,
    path_to_output_zip_folder: str,
    path_to_model: str,
    path_to_land_map: str,
) -> str:
    unique_name = generate_unique_name(path_to_tif)

    shapefile_path = path_to_save_folder + unique_name + ".shp"
    output_boxed_jpg_path = path_to_save_folder + unique_name + "_boxed.jpg"
    output_csv_path = path_to_save_folder + unique_name + ".csv"
    output_zip_path = path_to_output_zip_folder + unique_name + "_archive.zip"

    transform, coordinates = read_geospatial_metadata_from_tif(path_to_tif)

    img = convert_image(path_to_tif)

    track_results, names = detect_objects_in_image(img, path_to_model)

    annotated_img = annotate_tracking_results(img, track_results, names)
    cv.imwrite(output_boxed_jpg_path, annotated_img)

    buildings = process_detection_results(
        path_to_land_map,
        track_results,
        names,
        transform,
        coordinates,
    )
    create_buildings_shapefile(
        buildings,
        shapefile_path,
    )
    create_result_csv(buildings, output_csv_path)

    path_to_zip = archive_and_delete_files(
        unique_name, path_to_save_folder, output_zip_path
    )

    return path_to_zip


def analyze_photo(
    img,
    path_to_model,
    path_to_land_map,
    transform,
    coordinates,
    buildings_count: int = 1,
):  # TODO

    track_results, names = detect_objects_in_image(img, path_to_model)

    annotated_img = annotate_tracking_results(img, track_results, names)

    buildings = process_detection_results(
        path_to_land_map, track_results, names, transform, coordinates, buildings_count
    )

    return annotated_img, buildings


start = time.time()
analyze_tif(
    "без_зданий.tif",
    "service/ml/src/result/",
    "result/",
    "model_100epochs_second.pt",
    "land plots/Kimovsk/ZU.shp",
)
print(f"Полное время выполнения функции проходит за: {time.time() - start} секунд")
