import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
import re


def parse_vol(name: str):
    """
    >>> parse_vol("Сидр Заповедник Black Currant Friday 0,33 бут.")
    '0,33 бут.'
    >>> parse_vol("Af Brew Chori Chori Chupke Chupke 0,45 бан.")
    '0,45 бан.'
    >>> parse_vol("Af Brew Chori Chori Chupke Chupke 0.5 бут.")
    '0.5 бут.'
    >>> parse_vol("De Cam Wilde Bosbessen Fruit lambic 0.75 Aged")
    '0.75'
    >>> parse_vol("Kaiser Brau Liebenweiss Hefe Weissbier 0,5 бут")
    '0,5 бут'
    >>> parse_vol('Grossmeister св. 0,5л бан.')
    '0,5л бан.'
    >>> parse_vol('Bfm Abbaye De Saint Bon-Chien 2015 темн. 0,75л.')
    '0,75л.'
    >>> parse_vol("Oud Beersel Oude Geuze Vieille Whiskey Edition Portwood 2022 0,75 бут.")
    '0,75 бут.'
    """
    try:
        return re.findall(r'\d+[,.]\d+л?\.?\s*(?:бут|бан)?\.?', name)[0].strip()
    except IndexError:
        try:
            return re.findall(r"(\d+[,.]\d+) Aged", name)[0]
        except IndexError:
            raise ValueError(f"Не удалось разобрать объем пива из названия '{name}'")


def clean_name_and_parse_vol(name: str, brewery: str):
    """
    >>> clean_name_and_parse_vol("Сидр Заповедник Black Currant Friday 0,33 бут.", "Заповедник")
    ('Black Currant Friday', '0,33 бут.')
    >>> clean_name_and_parse_vol("Af Brew Chori Chori Chupke Chupke 0,45 бан.", "Af Brew")
    ('Chori Chori Chupke Chupke', '0,45 бан.')
    >>> clean_name_and_parse_vol("Af Brew Zero-Zero Takeoff 1 0,33 бан., б/а", "Af Brew")
    ('Zero-Zero Takeoff 1', '0,33 бан.')
    >>> clean_name_and_parse_vol("3 Fonteinen Aardbei Oogst 2022 Season 22/23 Blend No 41 0,75 бут.", "3 Fonteinen")
    ('Aardbei Oogst 2022 Season 22/23 Blend No 41', '0,75 бут.')
    >>> clean_name_and_parse_vol("3 Fonteinen Oude Geuze (season 18|19) Blend No. 50 св. 1,5 бут.", "3 Fonteinen")
    ('Oude Geuze (season 18|19) Blend No. 50 св.', '1,5 бут.')
    >>> clean_name_and_parse_vol("Чаща Trickster Smoked Chipotle Scotch Bonnet 0,5 бан.", "Чаща")
    ('Trickster Smoked Chipotle Scotch Bonnet', '0,5 бан.')
    >>> clean_name_and_parse_vol("Чай Steppe& Wind Шен Пуэр Малина Гранат 0,33 бан.", "Steppe&Wind")
    ('Шен Пуэр Малина Гранат', '0,33 бан.')
    >>> clean_name_and_parse_vol("Сидр Соколиные Сады Apple Queen Semi Sweet 0,45 бут.", "Соколиные Сады")
    ('Apple Queen Semi Sweet', '0,45 бут.')
    >>> clean_name_and_parse_vol("Сидр Ш Вишня 0,45 бут.", "Сидр Ш")
    ('Ш Вишня', '0,45 бут.')
    >>> clean_name_and_parse_vol("Мёд Steppe& Wind Smoothie Mead Raspberry Black Currant Mint 0,45 бан.", "Steppe&Wind")
    ('Smoothie Mead Raspberry Black Currant Mint', '0,45 бан.')
    >>> clean_name_and_parse_vol("[Aged]Hanssens Oude Kriek Sсhaarbeekse темн. 0,375 бут.", "Hanssens Artisanaal")
    ('Hanssens Oude Kriek Sсhaarbeekse', '0,375 бут.')
    >>> clean_name_and_parse_vol("Palm 0,5 бан.", "Palm")
    ('Palm', '0,5 бан.')
    """
    for prefix_to_remove in ("Сидр", "Чай", "Мёд", "[Aged]"):
        # Удаляем "Сидр" из начала названия, если оно есть
        if name.startswith(prefix_to_remove):
            name = name[len(prefix_to_remove):]
    name = name.strip()

    vol = parse_vol(name)
    name = name.replace(vol, "")
    name = name.strip()

    for suffix_to_remove in ("темн.", ", б/а"):
        if name.endswith(suffix_to_remove):
            name = name[:-len(suffix_to_remove)]
    name = name.strip()

    # Удаляем название пивоварни из начала строки
    breweries_to_remove = [brewery]
    if brewery == "Steppe&Wind":
        breweries_to_remove.append("Steppe& Wind")

    for brewery in breweries_to_remove:
        if brewery in name:
            replaced = name.replace(brewery, "", 1).strip()
            if replaced and not replaced.startswith("&"):
                name = replaced

    return name, vol


def parse_and_save_beers(html: str, shop: str, sqlite_connection):
    """
    Парсит HTML-страницу с пивом из магазина и сохраняет данные в SQLite.

    Args:
        html: HTML-строка для парсинга
        shop: Название магазина
        sqlite_connection: Соединение с SQLite
    """
    soup = BeautifulSoup(html, "html.parser")

    # Находим контейнер с бутылками
    bottles_div = soup.find("div", id="bottles")
    if not bottles_div:
        print("Не найден блок с бутылками (#bottles)")
        return

    # Находим таблицу внутри блока
    table = bottles_div.find("table")
    if not table:
        print("Таблица не найдена внутри #bottles")
        return

    # Создаем таблицу в БД, если её нет
    cursor = sqlite_connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS beruvyhodnoy_beers (
        shop TEXT,
        country TEXT,
        name TEXT,
        style TEXT,
        density TEXT,
        alcohol TEXT,
        brewery TEXT,
        price TEXT,
        date TEXT,
        vol TEXT
    )
    """
    )

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Находим все строки в таблице
    rows = table.find_all("tr")

    current_country = ""
    i = 0
    while i < len(rows):
        row = rows[i]

        # Проверяем, является ли строка заголовком страны
        header_cell = row.find("td", class_="header")
        if header_cell:
            current_country = header_cell.text.strip()
            i += 1
            continue

        # Проверяем, является ли строка заголовком колонок
        if row.find("th"):
            i += 1
            continue

        # Обрабатываем строку с данными
        cells = row.find_all(["td"])
        if len(cells) >= 7:
            # Извлекаем данные
            name = cells[1].text.strip()
            style = cells[2].text.strip()
            density = cells[3].text.strip()
            alcohol = cells[4].text.strip()
            brewery = cells[5].text.strip()
            price = cells[6].text.strip()

            name, vol = clean_name_and_parse_vol(name, brewery)


            # Удаляем символ рубля для хранения только числа
            price = price.replace("₽", "").strip()

            # Вставляем данные в БД
            cursor.execute(
                """
            INSERT INTO beruvyhodnoy_beers 
            (shop, country, name, style, density, alcohol, brewery, price, date, vol)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    shop,
                    current_country,
                    name,
                    style,
                    density,
                    alcohol,
                    brewery,
                    price,
                    current_date,
                    vol,
                ),
            )

        i += 1

    # Сохраняем изменения
    sqlite_connection.commit()


if __name__ == "__main__":
    shops = [
        ("Проспект Мира, 79", "beruvyhodnoy_14.html"),
        ("ул. Строителей 7к1", "beruvyhodnoy_29.html"),
        ("ул. Пивченкова, 7", "beruvyhodnoy_32.html"),
    ]

    with sqlite3.connect("../beer.db") as conn:
        for shop_name, shop_html in shops:
            with open(shop_html, "r", encoding="utf-8") as f:
                html = f.read()
                parse_and_save_beers(html, shop_name, conn)
