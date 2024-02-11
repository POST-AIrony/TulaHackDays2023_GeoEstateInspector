import os
from random import randint
from zipfile import ZipFile
from PIL import Image


def convert_tif_to_jpg(path_to_image, output_folder):
    """
    Конвертирует изображение из формата TIFF в формат JPEG.

    Parameters
    ----------
    path_to_image : str
        Путь к файлу изображения в формате TIFF, который требуется конвертировать.
    output_folder : str, optional
        Путь к папке, куда будет сохранен конвертированный файл в формате JPEG. 
        По умолчанию используется папка "result".

    Returns
    -------
    str
        Путь к конвертированному файлу в формате JPEG.

    Пример
    -------
    >>> convert_tif_to_jpg("/путь/к/файлу/изображение.tif", "output")
    "output/изображение.jpg"
    """
    
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
        print(f"Лог из разряда Converted {path_to_image} to {output_path}")
        return output_path


def archive_and_delete_files(name, path_to_save_folder, path_to_output_zip_folder):
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
    files_to_archive = [f for f in os.listdir(path_to_save_folder) if f.startswith(name)]

    # Проверка наличия файлов для архивации
    if not files_to_archive:
        print("Файлы куда-то испарились...")
        return None

    # Создание ZIP-архива
    zip_file_path = os.path.join(path_to_output_zip_folder, f"{name}_archive.zip")
    with ZipFile(zip_file_path, "w") as zipfile:
        for file_name in files_to_archive:
            file_path = os.path.join(path_to_save_folder, file_name)
            
            # Добавление файла в архив
            zipfile.write(file_path, os.path.basename(file_path))

    # Удаление заархивированных файлов
    for file_name in files_to_archive:
        file_path = os.path.join(path_to_save_folder, file_name)
        os.remove(file_path)

    print(f"Файлы от {name} Заархивированы и удалены. Архив создан: {zip_file_path}")
    print("тут логи")

    # Возвращение пути к созданному ZIP-архиву
    return zip_file_path


def is_tiff(filename):
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
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() == ".tiff"


def generate_unique_name(path_to_file):
    """
    Генерирует уникальное имя на основе пути к файлу.

    Parameters
    ----------
    path_to_file : str
        Путь к файлу, на основе которого будет создано уникальное имя.

    Returns
    -------
    str
        Уникальное имя файла, сгенерированное на основе пути к файлу.

    Пример
    -------
    >>> generate_unique_name("/путь/к/файлу/файл.txt")
    'файл_7234'
    """
    name = (
        os.path.splitext(os.path.basename(path_to_file))[0]
        + "_"
        + str(randint(5, 10000))
    )
    return name
