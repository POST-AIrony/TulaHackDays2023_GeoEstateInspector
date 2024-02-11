from core.MapCreator import find_parcel_for_building
from core.ResultCreator import write_results_to_pdf
from core.YoloTracker import image_processing
from core.FilesPreprocessor import archive_and_delete_files, generate_unique_name


def analyze_tiff(path_to_tif, path_to_save_folder,  path_to_model, path_to_land_map):
    unique_name = generate_unique_name(path_to_tif)
    image_processing(path_to_tif, path_to_save_folder, path_to_model, unique_name)
    results = find_parcel_for_building(unique_name, path_to_save_folder, path_to_land_map)
    write_results_to_pdf(results, unique_name, path_to_save_folder)
    path_to_zip = archive_and_delete_files(unique_name, path_to_save_folder)
    return path_to_zip


def analyze_photo(path_to_file, path_to_save_folder, path_to_model, path_to_land_map):
    name = True  # to do
    results = find_parcel_for_building(name, path_to_land_map)
    return f"{name}.jpg", results
