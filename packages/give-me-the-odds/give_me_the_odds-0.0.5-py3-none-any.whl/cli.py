#!/usr/bin/env python3

import click
import os

from db.db import init_db
from db.route import Route
from models.millenium_falcon import MilleniumFalcon
from models.empire import Empire
from odds.odds import compute_odds


def _load_db(routes_db: str) -> None:
    db_path: str = os.path.join(os.getcwd(), routes_db)
    return init_db(f"sqlite:////{db_path}")


@click.command()
@click.argument("millenium_falcon", type=click.File("r"))
@click.argument("empire", type=click.File("r"))
def give_me_the_odds(millenium_falcon, empire):
    falcon: MilleniumFalcon = MilleniumFalcon.parse(
        millenium_falcon.read())
    empire_data: Empire = Empire.parse(empire.read())
    db_session = _load_db(falcon.routes_db)
    routes: list[Route] = Route.query.all()
    odds: float = compute_odds(falcon, routes, empire_data)
    print(round(odds * 100.0))
    db_session.remove()


if __name__ == "__main__":
    give_me_the_odds()
