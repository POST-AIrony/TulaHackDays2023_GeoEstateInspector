import numpy as np
from PIL import Image
from ultralytics import YOLO
from FilesPreprocessor import convert_tif_to_jpg
from MapCreator import TakeInfoFromTif, CreateShapefile


def load_model(model_path):
    """
    Загружает модель YOLO для детекции объектов.

    Parameters:
    - model_path (str): Путь к файлу модели.

    Returns:
    - YOLO: Загруженная модель YOLO.
    """
    return YOLO(model_path, task="detect")


def image_processing(path_to_tif, path_to_save_folder, model_path, unique_name):
    """
    Обрабатывает изображение в формате TIFF, используя модель YOLO для детекции объектов.

    Parameters:
    - path_to_tif (str): Путь к файлу изображения формата TIFF.

    Returns:
    - результат выполнения функции find_parcel_for_building.
    """
    print('тут логи "фото обработалось такое то"')
    model = load_model(model_path)
    names = model.names

    # Конвертация из TIFF в JPEG
    path_to_jpg = convert_tif_to_jpg(path_to_tif, output_folder=path_to_save_folder)
    img = Image.open(path_to_jpg)
    img = np.ascontiguousarray(img)

    # Получение предсказаний модели YOLO
    results = model.predict(img)
    # Путь к выходным файлам
    output_shapefile_path = path_to_save_folder + unique_name + ".shp"
    output_boxed_jpg_path = path_to_save_folder + unique_name + "_boxed.jpg"

    transform, coordinates = TakeInfoFromTif(path_to_tif)

    CreateShapefile(
        output_shapefile_path,
        output_boxed_jpg_path,
        results,
        names,
        transform,
        coordinates,
        img,
    )


image_processing(
    "kimovsk2022-23-14.tif",
    "result/",
    "model_100epochs_second.pt",
    "test",
)
