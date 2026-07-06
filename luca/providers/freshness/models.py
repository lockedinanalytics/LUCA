from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel


class ProviderFreshness(BaseModel):
    provider: str
    status: str
    last_updated_utc: str | None = None
    max_age_seconds: int | None = None
    age_seconds: int | None = None
    warning: str | None = None


def freshness_report(provider: str, last_updated_utc: str | None, max_age_seconds: int) -> ProviderFreshness:
    if not last_updated_utc:
        return ProviderFreshness(provider=provider, status="missing", max_age_seconds=max_age_seconds, warning="No timestamp available.")

    dt = datetime.fromisoformat(last_updated_utc.replace("Z", "+00:00"))
    age = int((datetime.now(timezone.utc) - dt).total_seconds())

    if age <= max_age_seconds:
        status = "fresh"
        warning = None
    else:
        status = "stale"
        warning = f"Provider data is older than {max_age_seconds} seconds."

    return ProviderFreshness(
        provider=provider,
        status=status,
        last_updated_utc=last_updated_utc,
        max_age_seconds=max_age_seconds,
        age_seconds=age,
        warning=warning,
    )
