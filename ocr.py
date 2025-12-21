from paddleocr import PaddleOCR
import os

ocr_model = PaddleOCR(use_angle_cls=True, lang="en")

def run_ocr(image_path):
    if not os.path.exists(image_path):
        return ""

    result = ocr_model.ocr(image_path, cls=True)
    text = []
    for line in result:
        for word in line:
            text.append(word[1][0])
    return " ".join(text)
