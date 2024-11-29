import re

import parse

# todo  свет.0 5 с/б
#   Brewlab Белка Летяга свет.0 5 с/б


def clean_style(raw):
    return raw.title().strip()

@parse.with_pattern(r"|".join([
    'БАН.', 'БУТ.', 'БОКАЛ', 'БОКАЛ.', 'БУТ'
]))
def parse_tare(text):
    return text


@parse.with_pattern(r"|".join([
    '\d+,\d+', '\d+.\d+',
    '0,\d+X\d+', '\d+ X 0,\d+',
]))
def parse_volume(text):
    return text


@parse.with_pattern(r"|".join([
    'СВ.', 'КРАСН.', 'ТЕМН.', 'ТЕМ.', 'Б/А.',
    'полусухой', 'полусладкий',
]))
def parse_color(text):
    return text


parsers = {"color": parse_color, "tare": parse_tare, "volume": parse_volume}

def clean_clean_beru_vyh_brewery(raw_brewery: str) -> str:
    """
    >>> clean_clean_beru_vyh_brewery('Molson Coors (Usa)')
    'Molson Coors'
    >>> clean_clean_beru_vyh_brewery("Salden'S")
    'Saldens'
    """
    brewery = raw_brewery.title()
    brewery = re.sub("\(.*?\)", '', brewery)
    brewery = re.sub("'S", 's', brewery)
    return brewery.strip()

def clean_beru_vyh_title(raw_title: str) -> str:
    """
    >>> clean_beru_vyh_title('[АКЦИЯ] [40] 6°NORTH GRAN FONDO СВ. 0,44 БАН.')
    '6°NORTH GRAN FONDO'
    >>> clean_beru_vyh_title('[AGED]BREKERIET TILDA SOUR ALE СВ. 0,375 БУТ.')
    'BREKERIET TILDA SOUR ALE'
    >>> clean_beru_vyh_title("ALA NOVA DARK CLASSIC 0,45 БУТ.")
    'ALA NOVA DARK CLASSIC'
    >>> clean_beru_vyh_title('3 FONTEINEN KWEEPEER (SEASON 21|22) BLEND NO. 7 КРАСН. 0,75 БУТ.')
    '3 FONTEINEN KWEEPEER BLEND NO. 7'
    >>> clean_beru_vyh_title('STEENBRUGGE DUBBEL BRUIN ТЕМН. 0,33 БУТ.')
    'STEENBRUGGE DUBBEL BRUIN'
    >>> clean_beru_vyh_title('НАБОР BLANCHE DE BRUXELLES 0,33X3 БУТ. + БОКАЛ')
    'BLANCHE DE BRUXELLES'
    >>> clean_beru_vyh_title("НАБОР HUYGHE DISCOVER DELIRIUM SELECTION 4 X 0,33 БУТ. + БОКАЛ")
    'HUYGHE DISCOVER DELIRIUM SELECTION'
    >>> clean_beru_vyh_title('НАБОР VAN STEENBERGE GULDEN DRAAK (CLASS/QUAD/BREW/IMPST/SMOKED) 5 X 0,33 + БОКАЛ.')
    'VAN STEENBERGE GULDEN DRAAK'
    >>> clean_beru_vyh_title("EIBAU ZITTAUER BURGERBRAU HEFEWEIZEN 0,5 БАН.")
    'EIBAU ZITTAUER BURGERBRAU HEFEWEIZEN'
    >>> clean_beru_vyh_title('BURNING HOT! TOMATO GOSE WITH MUSHROOMS AND DATES 0,45 БАН.')
    'BURNING HOT! TOMATO GOSE WITH MUSHROOMS AND DATES'
    >>> clean_beru_vyh_title("CHIBIS ПЧЕЛА ПРИНЕСЛА ИВАН-ЧАЙ ВИШНЯ СВ. 0,5 БАН.")
    'CHIBIS ПЧЕЛА ПРИНЕСЛА ИВАН-ЧАЙ ВИШНЯ'
    >>> clean_beru_vyh_title('REBEL APPLE СИДР ТРАДИЦИОННЫЙ "DICKIY CREST ORIGINAL" СУХОЙ СВ. 0,5 БУТ.')
    'REBEL APPLE СИДР ТРАДИЦИОННЫЙ DICKIY CREST ORIGINAL СУХОЙ'
    >>> clean_beru_vyh_title('STEPPE& WIND SMOOTHIE MEAD: BLUEBERRIES,BANANA&VANILLA MEAD СВ. 0,45 БАН.')
    'STEPPE WIND SMOOTHIE MEAD BLUEBERRIES BANANA VANILLA MEAD'
    >>> clean_beru_vyh_title("TOKSOVO GOSE POINT: JALAPEÑO& LIME. VINTAGE 2022 СВ. 0,33 БУТ.")
    'TOKSOVO GOSE POINT JALAPEÑO LIME. VINTAGE 2022'
    >>> clean_beru_vyh_title("[АКЦИЯ] [40] PARADOX NEON FIELDS: MANGO, PEACH & CINNAMON SOUR ALE СВ. 0,5 БАН.")
    'PARADOX NEON FIELDS MANGO PEACH CINNAMON SOUR ALE'
    >>> clean_beru_vyh_title('ЛОСЬ И КЕДР MEAD \"ЛИК\" # 4 БРУСНИКА СВ. 0,33 БУТ.')
    'ЛОСЬ И КЕДР MEAD ЛИК # 4 БРУСНИКА'
    >>> clean_beru_vyh_title("[AGED] 3 FONTEINEN DRUIF/KRIEK DORNFELDER (SEASON 21|22) BLEND NO. 28 0,75 БУТ.")
    '3 FONTEINEN DRUIF/KRIEK DORNFELDER BLEND NO. 28'
    >>> clean_beru_vyh_title("Sindrom Velociraptor Strong Mead with Red Grape Tangerine Mixed Fermentation тем.")
    'Sindrom Velociraptor Strong Mead with Red Grape Tangerine Mixed Fermentation'
    """
    title = raw_title

    for pattern, repl in [
        ('НАБОР', ''),
        (r'\[\w+\]', ''),
        (' ', ' '),
        (r'\(.*?\)', ''),
    ]:
        title = re.sub(pattern, repl, title)
    title = title.strip()

    for format_ in [
        '{title}{:^tare}',
        '{title}{:^volume}',
        '{title}{:^color}'
    ]:
        while (parsed := True):
            parsed = parse.parse(
                format_, title, extra_types=parsers
            )
            if parsed:
                title = parsed['title'].strip(' +')
            else:
                break

    for pattern, repl in [
        (r'"', ''),
        (r'&', ' '),
        (r':', ' '),
        (r',', ' '),
        (r'\s+', ' '),
    ]:
        title = re.sub(pattern, repl, title)
    title = title.strip()

    title = title.strip(' +')

    return title
