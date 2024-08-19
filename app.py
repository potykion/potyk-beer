import dataclasses
import json
import sqlite3
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


app = flask.Flask(__name__)


@app.route("/")
def index_route():
    return flask.render_template("index.html")


@app.route("/styles")
def styles_route():
    q = Q(sqlite_conn_or_cursor=sqlite3.connect("beer.db", check_same_thread=False))
    styles = q.select_all("select * from beer_styles", as_=BeerStyle.from_row)

    return flask.render_template(
        "styles.html",
        styles=styles,
    )


if __name__ == "__main__":
    app.run(port=5001)
