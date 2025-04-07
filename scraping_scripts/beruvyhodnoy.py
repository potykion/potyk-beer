import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime


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
        date TEXT
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

            # Удаляем символ рубля для хранения только числа
            price = price.replace("₽", "").strip()

            # Вставляем данные в БД
            cursor.execute(
                """
            INSERT INTO beruvyhodnoy_beers 
            (shop, country, name, style, density, alcohol, brewery, price, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                ),
            )

        i += 1

    # Сохраняем изменения
    sqlite_connection.commit()


if __name__ == "__main__":
    # shop = ("Ул. Пивченкова, 7", "beruvyhodnoy_32.html")
    # shop_name, shop_html = ("Проспект Мира, 79", "beruvyhodnoy_14.html")
    shop_name, shop_html = ("ул. Строителей 7к1", "beruvyhodnoy_29.html")

    # Пример использования
    # with open(, "r", encoding="utf-8") as f:
    with open(shop_html, "r", encoding="utf-8") as f:
        html = f.read()

    with sqlite3.connect("../beer.db") as conn:
        parse_and_save_beers(html, shop_name, conn)
    pass
