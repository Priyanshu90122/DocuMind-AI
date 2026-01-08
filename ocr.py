from paddleocr import PaddleOCR
import os
import time

ocr_model = PaddleOCR(use_angle_cls=True, lang="en")


def run_ocr(image_path):
    if not image_path or not os.path.exists(image_path):
        return ""

    result = ocr_model.ocr(image_path)

    extracted_text = []
    if result:
        for line in result:
            for word in line:
                extracted_text.append(word[1][0])

    return " ".join(extracted_text).strip()
