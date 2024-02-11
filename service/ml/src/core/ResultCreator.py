from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def write_results_to_pdf(results, name, path_to_save_folder):
    """
    Создает PDF-документ с результатами обработки и включает в него информацию о зданиях и изображение с обозначенными рамками.

    Parameters:
    - results (list): Список словарей с информацией о зданиях и соответствующих им земельных участках.
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - Результат выполнения функции archive_and_delete_files.
    """
    print("Лог о создании pdf")

    # Путь к PDF-документу
    pdf_path = path_to_save_folder + name + ".pdf"
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
    image_reader = ImageReader(path_to_save_folder + name + "_boxed.jpg")
    c.drawImage(image_reader, 100, 100, width=500, height=500)

    # Сохранение PDF-документа
    c.save()
