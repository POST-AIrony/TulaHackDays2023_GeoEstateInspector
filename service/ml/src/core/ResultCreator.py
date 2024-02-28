from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ultralytics.utils.plotting import Annotator
import cv2


def create_results_pdf(results, output_pdf_path):
    print("Лог о создании pdf")

    pdf = canvas.Canvas(output_pdf_path, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    y_coordinate = 700

    for result in results:
        info_lines = [
            f"ID Здания: {result['building_id']}",
            f"Тип здания: {result['building_type']}",
            f"Местоположение здания: {result['building_position']}",
            f"ID кадастрового номера: {result['parcel_id']}",
            f"Кадастровый номер: {result['cadastral_']}",
        ]

        for line in info_lines:
            pdf.drawString(100, y_coordinate, line)
            y_coordinate -= 14
        pdf.showPage()
        y_coordinate = 700

    # Сохранение PDF-документа
    pdf.save()
    

def annotate_tracking_results(img, track_results, names):
    annotator = Annotator(img)
    for r in track_results:
            for box in r.boxes:
                b = box.xyxy[0]
                label = names[int(box.cls)]
                annotator.box_label(b, label, color=(79, 226, 104))
    return annotator.result()
    
