def classify_document(text):
    text = text.lower()
    if "invoice" in text:
        return "Invoice"
    if "aadhaar" in text or "uidai" in text:
        return "ID Document"
    return "Unknown"


def extract_fields(text):
    fields = {}
    if "₹" in text or "rs" in text.lower():
        fields["amount"] = "Detected"
    if "invoice" in text.lower():
        fields["invoice_number"] = "Detected"
    return fields


def validate(doc_type, fields):
    issues = []
    if doc_type == "Invoice" and "amount" not in fields:
        issues.append("Amount missing")
    if issues:
        return "INVALID", issues
    return "VALID", []


def decide(status):
    return "APPROVED" if status == "VALID" else "MANUAL REVIEW"


def explain(decision, issues):
    if decision == "APPROVED":
        return "All required fields detected. Document is valid."
    return "Issues found: " + ", ".join(issues)
