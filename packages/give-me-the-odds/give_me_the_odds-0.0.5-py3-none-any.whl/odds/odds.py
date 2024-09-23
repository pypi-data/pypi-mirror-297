from typing import Optional
from dataclasses import dataclass
from collections import deque

from db.route import Route
from models.millenium_falcon import MilleniumFalcon
from models.empire import Empire


@dataclass
class GraphEdge:
    weight: int
    node: str


@dataclass
class State:
    day: int
    planet: str
    fuel: int
    hunter_count: int


def _build_graph(routes: list[Route]) -> dict[str, list[GraphEdge]]:
    graph: dict[str, list[GraphEdge]] = {}

    for route in routes:
        if route.origin not in graph:
            graph[route.origin] = []
        if route.destination not in graph:
            graph[route.destination] = []

        graph[route.origin].append(
            GraphEdge(route.travel_time, route.destination))
        graph[route.destination].append(
            GraphEdge(route.travel_time, route.origin))

    return graph


def _compute_odds_from_hunter_count(hunter_count: int) -> float:
    return 0.9 ** hunter_count


def compute_odds(falcon: MilleniumFalcon, routes: list[Route], empire: Empire) -> float:
    graph: dict[str, list[GraphEdge]] = _build_graph(routes)
    start_state = State(0, falcon.departure, falcon.autonomy, 0)
    queue: deque[State] = deque([start_state])
    min_hunter_count: Optional[int] = None
    visited: dict[str, int] = {}

    while queue:
        state: State = queue.pop()

        # Out of fuel or out of time
        if state.fuel < 0 or state.day > empire.countdown:
            continue

        # if state.planet in visited and state.hunter_count >= visited[state.planet]:
        #     continue

        # visited[state.planet] = state.hunter_count

        # Arrived!
        if state.planet == falcon.arrival:
            if min_hunter_count is None or state.hunter_count < min_hunter_count:
                min_hunter_count = state.hunter_count
            continue

        # Check for bounty hunters
        for hunter in empire.bounty_hunters:
            if hunter.day == state.day and hunter.planet == state.planet:
                state.hunter_count += 1
                break

        # Wait/refuel
        queue.append(State(
            state.day + 1,
            state.planet,
            falcon.autonomy,
            state.hunter_count,
        ))

        # Travel
        for edge in graph[state.planet]:
            queue.append(State(
                state.day + edge.weight,
                edge.node,
                state.fuel - edge.weight,
                state.hunter_count,
            ))

    if min_hunter_count is None:
        return 0.0

    return _compute_odds_from_hunter_count(min_hunter_count)
