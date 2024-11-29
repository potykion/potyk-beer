import json

from beerlytics.beru_vyh.beru_vyh_beer import BeruVyhBeer
from beerlytics.beru_vyh.clean_beru_vyh import clean_beru_vyh_title, clean_style, clean_clean_beru_vyh_brewery


def parse_beru_vyh_beer(raw) -> BeruVyhBeer:
    """
    >>> parse_beru_vyh_beer(["154", "Plan B Iron Abyss", "Imperial Stout", "28", "11.0", "Plan B", "465₽"])
    BeruVyhBeer(number=154, title='Plan B Iron Abyss', style='Imperial Stout', og=28, abv=11.0, brewery='Plan B', price=465, raw_title='Plan B Iron Abyss')
    """
    raw = dict(zip(
        ['number', 'title', 'style', 'og', 'abv', 'brewery', 'price', 'country_or_type'],
        raw,
    ))
    return BeruVyhBeer(
        number=int(raw['number']),
        title=clean_beru_vyh_title(raw['title']),
        style=clean_style(raw['style'].strip()),
        og=int(raw['og']),
        abv=float(raw['abv']),
        brewery=clean_clean_beru_vyh_brewery(raw['brewery']),
        price=int(raw['price'].strip('₽')),
        raw_title=raw['title'],
        country_or_type=raw['country_or_type'],
    )


def read_and_parse_beru_vyh_beer(beru_vyh_json: str) -> list[BeruVyhBeer]:
    with open(beru_vyh_json, encoding='utf-8') as f:
        raw = json.load(f)
    beers = [parse_beru_vyh_beer(raw_beer) for raw_beer in raw]
    return beers
