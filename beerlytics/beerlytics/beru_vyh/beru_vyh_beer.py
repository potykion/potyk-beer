import dataclasses


@dataclasses.dataclass
class BeruVyhBeer:
    number: int
    title: str
    style: str
    og: int
    abv: float
    brewery: str
    price: int
    country_or_type: str
    raw_title: str
