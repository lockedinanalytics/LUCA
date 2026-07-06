from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel, Field

class ComponentHealth(BaseModel):
    name: str
    status: str = "unknown"
    freshness: str | None = None
    details: Dict[str, Any] = Field(default_factory=dict)

class SystemHealth(BaseModel):
    status: str
    version: str
    components: list[ComponentHealth]

def build_system_health(version: str = "0.4.0") -> SystemHealth:
    components = [
        ComponentHealth(name="kernel", status="operational"),
        ComponentHealth(name="feature_registry", status="operational"),
        ComponentHealth(name="analytics", status="operational"),
        ComponentHealth(name="sport_engines", status="operational"),
        ComponentHealth(name="objectives", status="operational"),
        ComponentHealth(name="governance", status="operational"),
        ComponentHealth(name="ledger", status="operational"),
        ComponentHealth(name="calibration", status="operational"),
        ComponentHealth(name="publication", status="operational"),
    ]
    return SystemHealth(status="ok", version=version, components=components)
