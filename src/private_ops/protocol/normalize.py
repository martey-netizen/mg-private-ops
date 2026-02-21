from __future__ import annotations


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) == 10:
        return f"+1{digits}"
    if digits.startswith("00"):
        return f"+{digits[2:]}"
    if digits.startswith("1") and len(digits) == 11:
        return f"+{digits}"
    if digits.startswith("+"):
        return digits
    return f"+{digits}" if digits else ""


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())
