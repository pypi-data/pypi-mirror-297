from __future__ import annotations
from dataclasses import dataclass
import json

from models.bounty_hunter import BountyHunter


@dataclass
class Empire:
    countdown: int
    bounty_hunters: list[BountyHunter]

    @classmethod
    def parse(cls, data: str) -> Empire:
        json_data: dict[str, any] = json.loads(data)
        bounty_hunter_data: list[dict[str, any]] = json_data["bounty_hunters"]
        return cls(
            json_data["countdown"],
            list(map(
                lambda bt_data: BountyHunter(
                    bt_data["planet"],
                    bt_data["day"],
                ),
                bounty_hunter_data,
            ))
        )

    def __repr__(self) -> str:
        return f"<Empire countdown={self.countdown} bounty_hunters={self.bounty_hunters}"
