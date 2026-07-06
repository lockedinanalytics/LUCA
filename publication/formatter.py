from luca.core.models import LucaRunResult, PickRecommendation

def public_pick_card(picks: list[PickRecommendation]) -> list[dict]:
    return [{"category":p.category.value,"pick":p.selection,"confidence":round(p.confidence,1),"units":p.units,"luca_status":p.governance_status.value} for p in picks]

def run_summary(result: LucaRunResult) -> dict:
    return {"sport":result.sport.value,"league":result.league,"date":result.date,"slate_size":result.slate_size,"games_evaluated":result.games_evaluated,"data_completeness":result.data_completeness,"run_status":result.run_status,"official_card":public_pick_card(result.recommendations)}
