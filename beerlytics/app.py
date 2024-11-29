import dataclasses
import json
import re
from operator import attrgetter, itemgetter
from typing import TypedDict, Dict, Any, List

import flask
from flask import Flask, render_template

from itertools import groupby

app = Flask(__name__)


class Brewery(TypedDict):
    """
    {"title": "Ayinger Privatbrauerei", "location": "Aying, Bayern Germany", "url": "https://untappd.com/AyingerBrewery/beer"},
    """

    title: str
    location: str
    url: str


class Beer(TypedDict):
    """
    {"title": "Ayinger Celebrator", "link": "https://untappd.com/b/ayinger-privatbrauerei-ayinger-celebrator/6683", "style": "Bock - Doppelbock", "abv": 6.7, "ibu": 24, "rating": 3.77, "ratingAmount": 168259, "added": "10/20/10", "mainStyle": "Bock", "subStyle": "Doppelbock", "breweryLink": "https://untappd.com/AyingerBrewery/beer"},
    """

    title: str
    link: str
    style: str
    abv: float
    ibu: float
    rating: float
    ratingAmount: int
    added: str
    mainStyle: str
    subStyle: str
    breweryLink: str


class BreweryWithBeers(TypedDict):
    """
    {"brewery":
    "beers": [{"title": "Ayinger Celebrator", "link": "https://untappd.com/b/ayinger-privatbrauerei-ayinger-celebrator/6683", "style": "Bock - Doppelbock", "abv": 6.7, "ibu": 24, "rating": 3.77, "ratingAmount": 168259, "added": "10/20/10", "mainStyle": "Bock", "subStyle": "Doppelbock", "breweryLink": "https://untappd.com/AyingerBrewery/beer"},
    """

    brewery: Brewery
    beers: list[Beer]


@dataclasses.dataclass
class BreweryStyleFreq:
    title: str = ""
    style_amount: int = 0
    url: str = ""
    beer_amount: int = 0
    beers: list[Beer] = dataclasses.field(default_factory=list)

    @property
    def id(self):
        """
        >>> BreweryStyleFreq(url='https://untappd.com/BierbrouwerijDeKoningshoeven/beer').id
        'BierbrouwerijDeKoningshoeven'
         >>> BreweryStyleFreq(url='https://untappd.com/w/ashram-cider/460729/beer').id
         'ashram-cider/460729'
        """
        return re.findall("https://untappd.com/w?/?(.*?)/beer", self.url)[0]

    @property
    def sort_label(self):
        return f"{self.mean_weighted_rating}<br>ratings: {self.sum_rating_amount}<br>beers: {self.style_amount} / {self.beer_amount}"

    @property
    def mean_weighted_rating(self):
        return round(sum((beer['rating']  * beer['ratingAmount'] for beer in self.beers)) / self.sum_rating_amount, 2)

    @property
    def sum_rating_amount(self):
        return sum(map(itemgetter('ratingAmount'), self.beers))

    @property
    def max_rating(self):
        return max(beer["rating"] for beer in self.beers)


    @property
    def sort_by(self):
        sort_param = (
            (sum((beer['rating']  * ((beer['ratingAmount'] ** 0.5) / (len(self.beers) ** 0.5)) for beer in self.beers)) / self.sum_rating_amount)
            # if len(self.beers) > 1 else
            # ((beer := self.beers[0])['rating']  / beer['ratingAmount'])
        )


        return (
            # -int(self.sum_rating_amount ** 0.5 / 10),
            -(self.mean_weighted_rating > 3.5),
            -(self.sum_rating_amount > 10000),
            -self.mean_weighted_rating,
            -self.sum_rating_amount
            # -sort_param,
            # -self.style_amount / self.beer_amount,
            # -self.style_amount,
        )


@app.get("/")
def styles_by_breweries_view():
    with open("beerlytics/untappd/beer_db.json", encoding="utf-8") as f:
        beer_db: list[BreweryWithBeers] = json.load(f)

    styles = sorted(
        {
            beer["style"]
            for brewery_w_beers in beer_db
            for beer in brewery_w_beers["beers"]
        }
    )

    limit = 8
    beer_filter = lambda beer: beer["ratingAmount"] > 500

    breweries_by_style_index = {}
    for brewery_w_beers in beer_db:
        brewery = brewery_w_beers["brewery"]
        beers = brewery_w_beers["beers"]
        beers = [beer for beer in beers if beer_filter(beer)]

        for beer in beers:
            breweries_by_style_index.setdefault(beer["style"], {})

            breweries_by_style_index[beer["style"]].setdefault(
                brewery["url"],
                BreweryStyleFreq(brewery["title"], 0, brewery["url"], len(beers)),
            )
            breweries_by_style_index[beer["style"]][brewery["url"]].style_amount += 1
            breweries_by_style_index[beer["style"]][brewery["url"]].beers.append(beer)

    breweries_by_style: dict[str, list[BreweryStyleFreq]] = {
        style: list(breweries.values())
        for style, breweries in breweries_by_style_index.items()
    }
    breweries_by_style: dict[str, list[BreweryStyleFreq]] = {
        style: sorted(breweries, key=attrgetter("sort_by"))
        for style, breweries in breweries_by_style.items()
    }

    styles = [style for style in styles if style in breweries_by_style]
    for style in styles:
        breweries_by_style.setdefault(style, [])
        breweries_by_style[style] = breweries_by_style[style][:limit] + [None] * (
            limit - len(breweries_by_style[style])
        )

    return render_template(
        "form.html",
        styles=styles,
        breweries_by_style=breweries_by_style,
    )


@app.get("/brewery")
def brewery():
    with open("beerlytics/untappd/beer_db.json", encoding="utf-8") as f:
        beer_db: list[BreweryWithBeers] = json.load(f)

    id = flask.request.args.get("id")

    brewery_w_beers = next(
        brewery_w_beers
        for brewery_w_beers in beer_db
        if id in brewery_w_beers["brewery"]["url"]
    )

    brewery = brewery_w_beers["brewery"]
    beers = brewery_w_beers["beers"]

    limit = 8

    beers_by_style = {
        style: sorted(style_beers, key=lambda beer: (beer['ratingAmount'], beer['rating']), reverse=True)
        for style, style_beers in groupby(
            sorted(beers, key=itemgetter("style")), itemgetter("style")
        )
    }
    beers_by_style = {
        style: (list(style_beers)[:limit] + [None] * max(0, limit - len(list(style_beers))))
        for style, style_beers in beers_by_style.items()
    }

    beers_by_style_sorted = sorted(beers_by_style.items(), key=lambda beers: -len(list(filter(None, beers[1]))))

    return render_template(
        "brewery.html",
        brewery=brewery,
        beers=beers,
        beers_by_style=beers_by_style_sorted,
    )
