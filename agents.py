def classify_document(text):
    text = text.lower()
    if "invoice" in text or "gst" in text:
        return "Invoice"
    if "aadhaar" in text or "uidai" in text:
        return "ID Document"
    if "agreement" in text or "contract" in text:
        return "Contract"
    if "receipt" in text or "paid" in text:
        return "Receipt"
    if "report" in text or "summary" in text:
        return "Report"
    return "Unknown"


def extract_fields(text):
    text_lower = text.lower()
    fields = {}

    if "₹" in text or "rs" in text_lower:
        fields["amount"] = "Detected"
    if "invoice" in text_lower:
        fields["invoice_number"] = "Detected"
    if "uidai" in text_lower or "aadhaar" in text_lower:
        fields["aadhaar_number"] = "Detected"
    if "date" in text_lower:
        fields["date"] = "Detected"
    if "signature" in text_lower:
        fields["signature"] = "Detected"

    return fields


def validate(doc_type, fields):
    issues = []

    if doc_type == "Invoice":
        if "amount" not in fields:
            issues.append("Amount missing")
        if "invoice_number" not in fields:
            issues.append("Invoice number missing")

    if doc_type == "ID Document":
        if "aadhaar_number" not in fields:
            issues.append("ID number missing")

    if doc_type == "Contract":
        if "signature" not in fields:
            issues.append("Signature missing")

    if doc_type == "Unknown":
        issues.append("Unrecognized document type")

    if issues:
        return "INVALID", issues
    return "VALID", []


def decide(status):
    return "APPROVED" if status == "VALID" else "MANUAL REVIEW"


def explain(decision, issues):
    if decision == "APPROVED":
        return "All required fields detected. Document is valid."
    return "Issues found: " + ", ".join(issues)
