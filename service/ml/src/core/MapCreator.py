import os
from datetime import datetime
from random import randint
from zipfile import ZipFile

import cv2
import fiona
import numpy as np
import pyproj
import rasterio
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from shapely.geometry import Point, Polygon, mapping, shape
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


# Определение схемы для нового Shapefile
schema = {
    "geometry": "Polygon",
    "properties": [("id", "int"), ("Name", "str"), ("cadastral_", "str")],
}


def find_parcel_for_building(name, path_to_land_map):
    """
    Идентифицирует земельные участки, на которых расположены здания, и создает новый Shapefile с результатами.

    Parameters:
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - Результат выполнения функции write_results_to_pdf.
    """
    print("Тут лог о том что мы ищем здания на фотке")

    # Открытие файлов Shapefile для зданий и земельных участков
    parcels = fiona.open(path_to_land_map, "r")
    buildings_shp_path = "result/" + name + ".shp"
    buildings = fiona.open(buildings_shp_path, "r")
    results = []

    # Получение CRS для земельных участков
    buildings_crs = pyproj.CRS.from_string(buildings.crs_wkt)
    parcels_crs = pyproj.CRS.from_string(parcels.crs_wkt)

    # Проверка наличия несоответствия CRS и создание трансформатора
    if buildings_crs != parcels_crs:
        transformer = pyproj.Transformer.from_crs(
            buildings_crs, parcels_crs, always_xy=True
        )
    else:
        transformer = None
        
    
    # Путь к новому Shapefile
    path = "result/" + name + "_with_parcel.shp"

    # Создание нового Shapefile и запись результатов
    with fiona.open(
        path, "w", driver="ESRI Shapefile", schema=schema, crs=buildings.crs
    ) as output:
        for building in buildings:
            building_polygon = shape(building["geometry"])
            building_center = building_polygon.centroid

            # Преобразование координат, если CRS различаются
            if buildings_crs != parcels_crs:
                lon, lat = transformer.transform(building_center.x, building_center.y)
                building_center = Point(lon, lat)
            found = False

            # Поиск соответствующего земельного участка
            for i, parcel in enumerate(parcels.values()):
                parcel_polygon = shape(parcel["geometry"])
                if building_center.within(parcel_polygon):
                    found = True
                    cadastral = parcel["properties"]["cadastral_"]
                    results.append(
                        {
                            "building_id": building["properties"]["id"],
                            "building_type": building["properties"]["Name"],
                            "building_position": (lon, lat),
                            "parcel_id": i,
                            "cadastral_": parcel["properties"]["cadastral_"],
                        }
                    )

            # Обработка случая, если земельный участок не найден
            if not found:
                cadastral = "Not found"
                results.append(
                    {
                        "building_id": building["properties"]["id"],
                        "building_type": building["properties"]["Name"],
                        "building_position": (lon, lat),
                        "parcel_id": "Not found",
                        "cadastral_": "Not found",
                    }
                )

            # Обновление информации о здании в новом Shapefile
            updated_building = {
                "geometry": building["geometry"],
                "properties": {
                    "id": building["properties"]["id"],
                    "Name": building["properties"]["Name"],
                    "cadastral_": cadastral,
                },
            }
            output.write(updated_building)

    # Закрытие файлов Shapefile
    buildings.close()
    parcels.close()

    # Вызов функции write_results_to_pdf для создания PDF-документа с результатами
    return results