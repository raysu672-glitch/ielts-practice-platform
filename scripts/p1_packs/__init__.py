# -*- coding: utf-8 -*-
"""Topic modules register Freestyle packs via register(_p)."""
from __future__ import annotations

from typing import Callable


def register_all(_p: Callable) -> None:
    from p1_packs import (
        science,
        feeling_bored,
        watch,
        cars,
        headphones,
        music,
        singing,
        shoes,
        clothing,
        mirrors,
        shopping,
        street_markets,
        fruit,
        rubbish_paper,
        tidiness,
        home,
        hometown,
        area_city,
        travelling,
        parks,
        tiredness_bored_extra,
        politeness_name,
        jokes,
        social_websites_ads,
        teachers_school,
        opportunities_work,
        space,
    )

    for mod in (
        science,
        feeling_bored,
        watch,
        cars,
        headphones,
        music,
        singing,
        shoes,
        clothing,
        mirrors,
        shopping,
        street_markets,
        fruit,
        rubbish_paper,
        tidiness,
        home,
        hometown,
        area_city,
        travelling,
        parks,
        tiredness_bored_extra,
        politeness_name,
        jokes,
        social_websites_ads,
        teachers_school,
        opportunities_work,
        space,
    ):
        mod.register(_p)
