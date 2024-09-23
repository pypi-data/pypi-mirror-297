from __future__ import annotations
from dataclasses import dataclass
import json


@dataclass
class BountyHunter:
    planet: str
    day: int

    @classmethod
    def parse(cls, data: str) -> BountyHunter:
        json_data: dict[str, any] = json.loads(data)
        return cls(
            json_data["planet"],
            json_data["day"],
        )

    def __repr__(self) -> str:
        return f"<BountyHunter planet={self.planet} day={self.day}"
