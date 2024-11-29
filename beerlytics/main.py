import sqlite3

import dataclasses
import json

from beerlytics.beru_vyh.beru_vyh_beer_parse import read_and_parse_beru_vyh_beer
from beerlytics.beru_vyh.json_to_sqlite import json_to_sqlite
from beerlytics.untappd.parse_untappd import UntappdBeer


def parse_beru_vyh():
    beers = read_and_parse_beru_vyh_beer('beru-vyh-assortea.json')
    json_beers = list(map(dataclasses.asdict, beers))
    with open('beerlytics/beru_vyh/beru_vyh_beers.json', 'w', encoding='utf-8') as f:
        json.dump(json_beers, f, ensure_ascii=False, indent=2)
    # duckdb.sql("select distinct brewery from 'beru_vyh_beers.json' order by brewery").write_csv('breweries.csv')
    # duckdb.sql("select country_or_type, style, count(style) from 'beru_vyh_beers.json' group by country_or_type, style order by country_or_type, count(style) desc ").write_csv('countries.csv')
    db = sqlite3.connect('beru_vyh_beers.sqlite')
    json_to_sqlite(db, 'beru_vyh_beers', json_beers)

def parse_untappd():
    with open('beerlytics/untappd/untappd-beers.json', encoding='utf-8') as f:
        raw = json.load(f)

    beers = [UntappdBeer.parse(beer) for beer in raw]
    json_beers = list(map(dataclasses.asdict, beers))

    db = sqlite3.connect('beru_vyh_beers.sqlite')
    json_to_sqlite(db, 'untappd_beers', json_beers)

if __name__ == '__main__':
    # parse_beru_vyh()
    parse_untappd()