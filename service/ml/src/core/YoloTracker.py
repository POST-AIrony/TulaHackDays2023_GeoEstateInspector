import numpy as np
from PIL import Image
from ultralytics import YOLO
from FilesPreprocessor import convert_tif_to_jpg
from MapCreator import TakeInfoFromTif, CreateShapefile


def load_yolo_detection_model(model_path):
    """
    Загружает модель YOLO для детекции объектов.

    Parameters:
    - model_path (str): Путь к файлу модели.

    Returns:
    - YOLO: Загруженная модель YOLO.
    """
    return YOLO(model_path, task="detect")


def detect_objects_in_image(img, path_to_model):
    print('тут логи "фото обработалось такое то"')
    model = load_yolo_detection_model(path_to_model)
    names = model.names

    # Получение предсказаний модели YOLO
    results = model.predict(img)
    
    return results, names