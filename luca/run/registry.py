from __future__ import annotations

from luca.core.models import Sport
from luca.core.engine import SportEngine
from luca.sports.mlb.engine import MlbEngine
from luca.sports.nfl.engine import NflEngine
from luca.sports.ncaaf.engine import NcaafEngine
from luca.sports.nba.engine import NbaEngine
from luca.sports.nhl.engine import NhlEngine
from luca.sports.soccer.engine import SoccerEngine
from luca.sports.golf.engine import GolfEngine
from luca.sports.tennis.engine import TennisEngine
from luca.sports.mma.engine import MmaEngine


def get_sport_engine(sport: Sport) -> SportEngine:
    engines = {
        Sport.MLB: MlbEngine(),
        Sport.NFL: NflEngine(),
        Sport.NCAAF: NcaafEngine(),
        Sport.NBA: NbaEngine(),
        Sport.NHL: NhlEngine(),
        Sport.SOCCER: SoccerEngine(),
        Sport.GOLF: GolfEngine(),
        Sport.TENNIS: TennisEngine(),
        Sport.MMA: MmaEngine(),
    }
    return engines[sport]
