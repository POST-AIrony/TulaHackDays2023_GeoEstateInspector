from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def WriteResultsToPdf(results, name, path_to_save_folder):
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
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    y_coordinate = 700

    # Добавление информации о зданиях в PDF
    for result in results:
        building_info = f"ID Здания: {result['building_id']}, Тип здания: {result['building_type']}, Местоположение здания: {result['building_position']}, ID кадастрового номера: {result['parcel_id']}, Кадастровый номер: {result['cadastral_']}"

        info_lines = building_info.split(", ")

        for line in info_lines:
            pdf.drawString(100, y_coordinate, line)
            y_coordinate -= 14
        pdf.showPage()
        y_coordinate = 700

    # Добавление изображения с обозначенными рамками в PDF
    pdf.showPage()
    image_reader = ImageReader(path_to_save_folder + name + "_boxed.jpg")
    pdf.drawImage(image_reader, 100, 100, width=500, height=500)

    # Сохранение PDF-документа
    pdf.save()
