from __future__ import annotations
from dataclasses import dataclass
import json


@dataclass
class MilleniumFalcon:
    autonomy: int
    departure: str
    arrival: str
    routes_db: str

    @classmethod
    def parse(cls, data: str) -> MilleniumFalcon:
        json_data: dict[str, any] = json.loads(data)
        return cls(
            json_data["autonomy"],
            json_data["departure"],
            json_data["arrival"],
            json_data["routes_db"],
        )
