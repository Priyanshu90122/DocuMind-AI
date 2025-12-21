from fastapi import FastAPI, UploadFile, File
import shutil
import os

from ocr import run_ocr
from agents import classify_document, extract_fields, validate, decide, explain
from database import save_log

app = FastAPI(title="OCR AI Agent System")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = run_ocr(path)
    os.remove(path)

    doc_type = classify_document(text)
    fields = extract_fields(text)
    status, issues = validate(doc_type, fields)
    decision = decide(status)
    explanation = explain(decision, issues)

    save_log(doc_type, decision, explanation)

    return {
        "ocr_text": text,
        "document_type": doc_type,
        "extracted_fields": fields,
        "decision": decision,
        "explanation": explanation
    }
