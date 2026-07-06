from __future__ import annotations


def mask_secret(value: str | None, visible: int = 4) -> str | None:
    if not value:
        return None
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]


def assert_no_secret_in_payload(payload: dict) -> dict:
    cleaned = dict(payload)
    for key in list(cleaned.keys()):
        if "key" in key.lower() or "token" in key.lower() or "secret" in key.lower():
            cleaned[key] = mask_secret(str(cleaned[key]))
    return cleaned
