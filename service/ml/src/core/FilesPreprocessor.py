import os
from zipfile import ZipFile
from PIL import Image



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

    print(
        f"Файлы от {name} Заархивированы и удалены. Архив создан: {zip_file_path}"
    )
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
    Генерирует уникальное имя для файла.

    Parameters:
    - path_to_tif (str): Путь к файлу изображения формата TIFF.

    Returns:
    - str: Уникальное имя файла.
    """
    name = os.path.splitext(os.path.basename(path_to_file))[0] + "_" + str(randint(5, 10000))
    return name