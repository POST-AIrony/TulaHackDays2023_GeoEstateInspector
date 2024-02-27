from MapCreator import find_parcel_for_building
from ResultCreator import WriteResultsToPdf
from YoloTracker import image_processing
from FilesPreprocessor import archive_and_delete_files, generate_unique_name


def analyze_tif(
    path_to_tif,
    path_to_save_folder,
    path_to_output_zip_folder,
    path_to_model,
    path_to_land_map,
):
    unique_name = generate_unique_name(path_to_tif)
    image_processing(path_to_tif, path_to_save_folder, path_to_model, unique_name)
    results = find_parcel_for_building(
        unique_name, path_to_save_folder, path_to_land_map
    )
    WriteResultsToPdf(results, unique_name, path_to_save_folder)
    path_to_zip = archive_and_delete_files(
        unique_name, path_to_save_folder, path_to_output_zip_folder
    )
    return path_to_zip


def analyze_photo(path_to_file, path_to_save_folder, path_to_model, path_to_land_map):
    name = True  # TODO
    results = find_parcel_for_building(name, path_to_land_map)
    return f"{name}.jpg", results
