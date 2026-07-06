from pydantic import BaseModel

class ComponentHealth(BaseModel):
    name: str
    status: str

def build_system_health(version: str="1.0.0-phase1") -> dict:
    comps=["kernel","providers","sports","objectives","governance","ledger","calibration","publication"]
    return {"status":"ok","version":version,"components":[ComponentHealth(name=c,status="operational").model_dump() for c in comps]}
