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


def convert_tif_to_jpg(path_to_image, output_folder="result"):
    """
    Конвертирует изображение в формате TIFF в формат JPEG.

    Parameters:
    - path_to_image (str): Путь к файлу изображения формата TIFF.
    - output_folder (str): Папка для сохранения конвертированного изображения в формате JPEG.

    Returns:
    - str: Путь к сохраненному изображению в формате JPEG.
    """
    print("тут логи")

    # Создание папки для сохранения, если её не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with Image.open(path_to_image) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # Создание пути к выходному файлу, заменяя расширение на .jpg
        output_path = os.path.join(
            output_folder, os.path.splitext(os.path.basename(path_to_image))[0] + ".jpg"
        )
        # Сохранение изображения в формате JPEG
        img.save(output_path, "JPEG")
        print(f"Converted {path_to_image} to {output_path}")
        return output_path


def archive_and_delete_files(name):
    """
    Архивирует временные файлы, создает ZIP-архив и удаляет исходные файлы.

    Parameters:
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - str or None: Путь к созданному ZIP-архиву или None, если файлы отсутствуют.
    """
    print("тут логи")

    # Получение списка файлов для архивации
    folder_path = "result/"
    files_to_archive = [f for f in os.listdir(folder_path) if f.startswith(name)]

    # Проверка наличия файлов для архивации
    if not files_to_archive:
        print("Файлы куда-то испарились...")
        return None

    # Создание ZIP-архива
    zip_file_path = os.path.join("static/from_ml", f"{name}_archive.zip")
    with ZipFile(zip_file_path, "w") as zipf:
        for file_name in files_to_archive:
            file_path = os.path.join(folder_path, file_name)
            # Добавление файла в архив
            zipf.write(file_path, os.path.basename(file_path))

    # Удаление заархивированных файлов
    for file_name in files_to_archive:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

    print(datetime.now())
    print(
        f"Файлы от {name} Заархивированы и удалены. Архив создан: {zip_file_path}"
    )
    print("тут логи")

    # Возвращение пути к созданному ZIP-архиву
    return zip_file_path
