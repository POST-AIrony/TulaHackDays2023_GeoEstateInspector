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


def write_results_to_pdf(results, name):
    """
    Создает PDF-документ с результатами обработки и включает в него информацию о зданиях и изображение с обозначенными рамками.

    Parameters:
    - results (list): Список словарей с информацией о зданиях и соответствующих им земельных участках.
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - Результат выполнения функции archive_and_delete_files.
    """
    print(datetime.now())
    print("PATH: /system/server.py -> write_results_to_pdf")

    # Путь к PDF-документу
    pdf_path = "result/" + name + ".pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    y_coordinate = 700

    # Добавление информации о зданиях в PDF
    for result in results:
        building_info = f"Building ID: {result['building_id']}, Building Type: {result['building_type']}, Building Position: {result['building_position']}, Parcel ID: {result['parcel_id']}, cadastral_: {result['cadastral_']}"

        info_lines = building_info.split(", ")

        for line in info_lines:
            c.drawString(100, y_coordinate, line)
            y_coordinate -= 14
        c.showPage()
        y_coordinate = 700

    # Добавление изображения с обозначенными рамками в PDF
    c.showPage()
    image_reader = ImageReader("result/" + name + "_boxed.jpg")
    c.drawImage(image_reader, 100, 100, width=500, height=500)

    # Сохранение PDF-документа
    c.save()