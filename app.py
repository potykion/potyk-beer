import dataclasses
import json
import sqlite3
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import TypedDict, Literal

import flask
from flask import render_template

from b3.q import Q

BASE_DIR = Path(__file__).parent


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
    sort_styles = flask.request.values.get("sort_styles", "name")

    beers = q.select_all(
        "select * from beer_my_untappd_beers order by style, rating desc", as_=MyBeer
    )
    beers_by_style = groupby(beers, key=lambda beer: beer["style"])
    beers_by_style = [(style, list(beers)) for style, beers in beers_by_style]

    if sort_styles == "name":
        beers_by_style = sorted(beers_by_style, key=lambda beer: beer[0])
    elif sort_styles == "amount":
        beers_by_style = sorted(
            beers_by_style, key=lambda beer: len(beer[1]), reverse=True
        )

    beers_by_brewery = groupby(
        sorted(beers, key=lambda beer: (beer["brewery"], -beer["rating"])),
        key=lambda beer: beer["brewery"],
    )
    beers_by_brewery = [(brewery, list(beers)) for brewery, beers in beers_by_brewery]
    beers_by_brewery = sorted(
        beers_by_brewery, key=lambda beer: len(beer[1]), reverse=True
    )

    return flask.render_template(
        "my_beers.html",
        beers_by_style=beers_by_style,
        beers_by_brewery=beers_by_brewery,
        sort_styles=sort_styles,
    )


class BeerPlace(TypedDict):
    id: int
    name: str
    city: str | None
    metro: str | None
    yandex_maps: str | None
    site: str | None
    telegram: str | None
    untappd: str | None
    untappd_verified: bool | None
    type: Literal[
        "Бар",
        "Магазин",
    ]


METRO_TO_COLOR = {
    "Маяковская": "🟢",
    "Новокузнецкая": "🟢",
    "Белорусская": "🟢",
    "Водный стадион": "🟢",
    "Южная": "🩶",
    "Арбатская": "🔵",
    "Бауманская": "🔵",
    "Электрозаводская": "🔵",
    "Славянский бульвар": "🔵",
    "Смоленская": "🔵",
    "Сходненская": "🟣",
    "Таганская": "🟣",
    "Пушкинская": "🟣",
    "Добрынинская": "🟤",
    "Чистые пруды": "🔴",
    "Лубянка": "🔴",
    "Кропоткинская": "🔴",
    "Красные Ворота": "🔴",
    "Университет": "🔴",
    "Китай-город": "🟠",
    "Сухаревская": "🟠",
    "Академическая": "🟠",

    "Раменки": "🟡",
}


@app.get("/admin")
def admin():


    return render_template("admin.html", )

@app.get("/admin/beer-places")
def admin_beer_places():
    connection = sqlite3.connect(
        BASE_DIR / "beer-places.sqlite", check_same_thread=False
    )
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    beer_places = cursor.execute("select * from beer_place order by name")
    beer_places = [BeerPlace(**row) for row in beer_places]

    beer_places_by_city = defaultdict(lambda: defaultdict(list))
    for beer_place in beer_places:
        beer_places_by_city[beer_place["city"]][beer_place["type"]].append(beer_place)

    md = render_template(
        "render/beer_places.md",
        beer_places_by_city=beer_places_by_city,
        METRO_TO_COLOR=METRO_TO_COLOR,
    )
    return f'    <pre><code>{md}</code></pre>'


if __name__ == "__main__":
    app.run(port=5001)
