import dataclasses
import json
import sqlite3
from itertools import groupby
from typing import TypedDict

import flask

from b3.q import Q


class BeerStyleExample(TypedDict):
    name: str
    untappd_link: str


class BeerStyle(TypedDict):
    id: int
    img: str
    name: str
    name_en: str
    description: str
    aroma: str
    taste: str
    texture: str
    alco: str
    bjcp_link: str
    bjcp_name: str
    examples: list[BeerStyleExample]

    @classmethod
    def from_row(cls, row):
        return {**row, "examples": json.loads(row["examples"])}


class MyBeer(TypedDict):
    id: int
    url: str
    name: str
    style: str
    brewery: str
    rating: float
    abv: float
    ibu: float
    img: str
    review: str
    style_id: int


app = flask.Flask(__name__)

q = Q(sqlite_conn_or_cursor=sqlite3.connect("beer.db", check_same_thread=False))


@app.route("/")
def index_route():
    return flask.render_template("index.html")


@app.route("/styles")
def styles_route():

    styles = q.select_all("select * from beer_styles", as_=BeerStyle.from_row)

    return flask.render_template(
        "styles.html",
        styles=styles,
    )


@app.route("/my-beers")
def my_beers_route():
    beers = q.select_all(
        "select * from beer_my_untappd_beers order by style, rating desc", as_=MyBeer
    )
    beers_by_style = groupby(beers, key=lambda beer: beer["style"])
    beers_by_style = [(style, list(beers)) for style, beers in beers_by_style]
    beers_by_style = sorted(beers_by_style, key=lambda beer: len(beer[1]), reverse=True)

    beers_by_brewery = groupby(
        sorted(beers, key=lambda beer: (beer["brewery"], -beer["rating"])),
        key=lambda beer: beer["brewery"],
    )
    beers_by_brewery = [(brewery, list(beers)) for brewery, beers in beers_by_brewery]
    beers_by_brewery = sorted(beers_by_brewery, key=lambda beer: len(beer[1]), reverse=True)

    return flask.render_template(
        "my_beers.html",
        beers_by_style=beers_by_style,
        beers_by_brewery=beers_by_brewery,
    )


if __name__ == "__main__":
    app.run(port=5001)
