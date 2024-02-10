import os
from datetime import datetime
from random import randint
import cv2
import fiona
import numpy as np
import rasterio
from PIL import Image
from shapely.geometry import Polygon, mapping
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from FilesPreprocessor import convert_tif_to_jpg


schema = {"geometry": "Polygon", "properties": [("id", "int"), ("Name", "str")]}


def load_model(model_path):
    """
    Загружает модель YOLO для детекции объектов.

    Parameters:
    - model_path (str): Путь к файлу модели.

    Returns:
    - YOLO: Загруженная модель YOLO.
    """
    return YOLO(model_path, task="detect")


def image_processing(path_to_tif, model_path, unique_name):
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
    path_to_jpg = convert_tif_to_jpg(path_to_tif)
    img = Image.open(path_to_jpg)
    img = np.ascontiguousarray(img)

    # Получение предсказаний модели YOLO
    results = model.predict(img)
    annotator = Annotator(img)
    features = []  # Предварительно выделенный список для хранения объектов
    # Путь к выходному файлу Shapefile
    output_shapefile_path = "result/" + unique_name + ".shp"

    with rasterio.open(path_to_tif) as src:
        transform = src.transform

        with fiona.open(
            output_shapefile_path,
            mode="w",
            driver="ESRI Shapefile",
            schema=schema,
            crs=src.crs,
        ) as shp:
            
            # Обработка результатов детекции
            for r in results:
                for id, box in enumerate(r.boxes, start=1):
                    b = box.xyxy[0]
                    label = names[int(box.cls)]
                    box_geo = [
                        transform * (b[0], b[1]),
                        transform * (b[0], b[3]),
                        transform * (b[2], b[3]),
                        transform * (b[2], b[1]),
                        transform * (b[0], b[1]),
                    ]

                    polygon = Polygon(box_geo)

                    row_dict = {
                        "geometry": mapping(polygon),
                        "properties": {"id": id, "Name": names[int(box.cls)]},
                    }
                    features.append(row_dict)
                    annotator.box_label(b, label, color=(79, 226, 104))
            shp.writerecords(features)

    # Сохранение изображения с обозначенными рамками в файл
    cv2.imwrite("result/" + unique_name + "_boxed.jpg", annotator.result())


image_processing("/home/rebelraider/Документы/Python projects/MachineLearning/Hackatons/tula/кимовск/kimovsk2022-25-15.tif",
                 "/home/rebelraider/Документы/Python projects/MachineLearning/Hackatons/TulaHackDays2023_GeoEstateInspector/server/model_100epochs_second.pt",
                 "test")