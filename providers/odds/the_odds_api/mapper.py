from __future__ import annotations

from luca.core.models import MarketLine, MarketType, TeamGame


def map_market_key(key: str) -> MarketType | None:
    if key == "h2h":
        return MarketType.MONEYLINE
    if key == "spreads":
        return MarketType.SPREAD
    if key == "totals":
        return MarketType.TOTAL
    return None


def odds_event_to_market_lines(event: dict, game: TeamGame | None = None) -> list[MarketLine]:
    game_id = game.game_id if game else str(event.get("id", "unknown"))
    output: list[MarketLine] = []

    for bookmaker in event.get("bookmakers", []):
        book = bookmaker.get("key") or bookmaker.get("title")
        for market in bookmaker.get("markets", []):
            market_type = map_market_key(market.get("key", ""))
            if market_type is None:
                continue

            for outcome in market.get("outcomes", []):
                selection = outcome.get("name", "")
                price = outcome.get("price")
                point = outcome.get("point")

                output.append(
                    MarketLine(
                        game_id=game_id,
                        market_type=market_type,
                        selection=selection,
                        book=book,
                        current_odds=float(price) if price is not None else None,
                        spread=float(point) if market_type == MarketType.SPREAD and point is not None else None,
                        total=float(point) if market_type == MarketType.TOTAL and point is not None else None,
                    )
                )

    return output
