from luca.core.models import Sport
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.workflows.pipeline import LucaWorkflowPipeline, PipelineContext

def test_workflow_static_run():
    pipeline = LucaWorkflowPipeline(StaticScheduleProvider(), StaticMarketProvider())
    result = pipeline.run(PipelineContext(sport=Sport.NFL, league="NFL", date="2026-08-01"))
    assert result.games_evaluated == 1
