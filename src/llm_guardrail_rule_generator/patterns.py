import re

# Common PII (Personally Identifiable Information) patterns
PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "us_phone": re.compile(r"\b(?:\+1[-.\s]?|1[-.\s]?)?(\(?\d{3}\)?|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "us_zip": re.compile(r"\b\d{5}(?:-\d{4})?\b"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "date_iso": re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
}

# Common PHI (Protected Health Information) patterns
PHI_PATTERNS = {
    "mrn": re.compile(r"\bMRN[:\s]*\d{6,10}\b", re.IGNORECASE),  # Medical Record Number
    "nhs_number": re.compile(r"\b\d{3} \d{3} \d{4}\b"),  # UK NHS number format
    "icd_code": re.compile(r"\b[A-Z]\d{2}(?:\.\d{1,4})?\b"),  # ICD-10 codes
    "health_insurance_id": re.compile(r"\bHIN[:\s]*[A-Z0-9]{8,12}\b", re.IGNORECASE),
}

# Common PCI (Payment Card Industry) patterns
PCI_PATTERNS = {
    "visa": re.compile(r"\b4[0-9]{12}(?:[0-9]{3})?\b"),
    "mastercard": re.compile(r"\b5[1-5][0-9]{14}\b"),
    "amex": re.compile(r"\b3[47][0-9]{13}\b"),
    "discover": re.compile(r"\b6(?:011|5[0-9]{2})[0-9]{12}\b"),
}

# Keywords that may indicate prompt injection attempts
PROMPT_INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "disregard all prior",
    "override the rules",
    "bypass the filter",
    "disable the guardrails",
    "ignore this message",
    "forget your instructions",
]

# Aggregate all patterns for easy access
ALL_PATTERNS = {
    "pii": PII_PATTERNS,
    "phi": PHI_PATTERNS,
    "pci": PCI_PATTERNS,
    "prompt_injection_keywords": PROMPT_INJECTION_KEYWORDS,
}

if __name__ == "__main__":
    # Simple demonstration of pattern matching
    sample_text = "Contact me at john.doe@example.com or call 555-123-4567. My SSN is 123-45-6789."
    for category, patterns in ALL_PATTERNS.items():
        if isinstance(patterns, dict):
            for name, pattern in patterns.items():
                matches = pattern.findall(sample_text)
                if matches:
                    print(f"Found {category} pattern '{name}': {matches}")
        elif isinstance(patterns, list):
            for keyword in patterns:
                if keyword in sample_text.lower():
                    print(f"Found prompt injection keyword: {keyword}")
