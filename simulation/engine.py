import math, random
from pydantic import BaseModel

class SimulationRequest(BaseModel):
    game_id: str
    runs: int=10000
    mean_home: float=4.5
    mean_away: float=4.2

def _poisson(lam: float) -> int:
    L=math.exp(-max(.05,lam)); k=0; p=1.0
    while p>L: k+=1; p*=random.random()
    return k-1

def simulate_game(req: SimulationRequest, seed: int|None=42) -> dict:
    if seed is not None: random.seed(seed)
    hw=0; hs=[]; aws=[]
    for _ in range(req.runs):
        h=_poisson(req.mean_home); a=_poisson(req.mean_away)
        if h==a: h+=1 if random.random()>=.5 else 0; a+=1 if h==a else 0
        hw += h>a; hs.append(h); aws.append(a)
    mh=sum(hs)/req.runs; ma=sum(aws)/req.runs
    return {"game_id":req.game_id,"runs":req.runs,"home_win_probability":hw/req.runs,"away_win_probability":1-hw/req.runs,"projected_home_score":round(mh,3),"projected_away_score":round(ma,3),"projected_total":round(mh+ma,3),"projected_margin":round(mh-ma,3)}
