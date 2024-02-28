import os
from random import randint
from zipfile import ZipFile
from PIL import Image
import numpy as np

def convert_tif_to_jpg(path_to_tif):
    with Image.open(path_to_tif) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")
            img = np.ascontiguousarray(img)
        print(f"Лог из разряда {path_to_tif} конвертирован в jpg")
        return img


def archive_and_delete_files(name, path_to_save_folder, output_zip_path):
    """
    Архивирует и удаляет файлы с определенным именем.

    Parameters
    ----------
    name : str
        Имя файлов, которые требуется архивировать и удалить.

    Returns
    -------
    str or None
        Путь к созданному ZIP-архиву, если файлы были архивированы и удалены успешно.
        Возвращает None, если файлы для архивации отсутствуют.

    Пример
    -------
    >>> archive_and_delete_files("example")
    "static/from_ml/example_archive.zip"
    """
    print("тут логи")

    # Получение списка файлов для архивации
    files_to_archive = [
        f for f in os.listdir(path_to_save_folder) if f.startswith(name)
    ]

    # Проверка наличия файлов для архивации
    if not files_to_archive:
        print("Файлы куда-то испарились...")
        return None

    # Создание ZIP-архива
    with ZipFile(output_zip_path, "w") as zipfile:
        for file_name in files_to_archive:
            file_path = os.path.join(path_to_save_folder, file_name)

            # Добавление файла в архив
            zipfile.write(file_path, os.path.basename(file_path))

            # Удаление заархивированного файла
            os.remove(file_path)

    print(f"Файлы от {name} Заархивированы и удалены. Архив создан: {output_zip_path}")
    print("тут логи")

    # Возвращение пути к созданному ZIP-архиву
    return output_zip_path


def is_tif_file(filename):
    """
    Проверяет, является ли файл формата .tiff по имени.

    Parameters
    ----------
    filename : str
        Имя файла для проверки.

    Returns
    -------
    bool
        True, если файл имеет расширение .tiff; в противном случае - False.

    Notes
    -----
    Эта функция использует метод os.path.splitext(), чтобы разделить путь к файлу на
    базовое имя и расширение файла. Затем она проверяет, является ли расширение .tiff,
    игнорируя регистр символов.

    Examples
    --------
    >>> is_tiff("image.tiff")
    True
    >>> is_tiff("document.txt")
    False
    """
    file_extension = os.path.splitext(filename)[1]
    return file_extension.lower() == ".tif"


def generate_unique_name(path_to_file):
    name = (
        os.path.splitext(os.path.basename(path_to_file))[0]
    )
    return name
