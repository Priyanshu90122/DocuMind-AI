from fastapi import FastAPI, UploadFile, File
import shutil
import os
import time

from ocr import run_ocr
from agents import classify_document, extract_fields, validate, decide, explain
from database import save_log

app = FastAPI(title="Production OCR Document Intelligence System")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    start_time = time.time()

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = run_ocr(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    document_type = classify_document(text)
    extracted_fields = extract_fields(text)
    status, issues = validate(document_type, extracted_fields)
    decision = decide(status)
    explanation = explain(decision, issues)

    processing_time = round(time.time() - start_time, 3)

    save_log(
        document_type=document_type,
        decision=decision,
        explanation=explanation,
        processing_time=processing_time
    )

    return {
        "ocr_text": text,
        "document_type": document_type,
        "decision": decision,
        "processing_time_seconds": processing_time,
        "extracted_fields": extracted_fields,
        "explanation": explanation
    }
