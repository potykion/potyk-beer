{% macro msk_place_location(place) -%}
{% if place.metro and place.yandex_maps -%}[{{ METRO_TO_COLOR[place.metro] }} {{ place.metro }}]({{ place.yandex_maps }}){% endif -%}
{% if not place.metro and place.yandex_maps -%}[:simple-googlemaps:]({{ place.yandex_maps }}){% endif -%}
{% if place.metro and not place.yandex_maps -%} {{ METRO_TO_COLOR[place.metro] }} {{ place.metro }} {% endif -%}
{%- endmacro -%}


{% macro place_name(place) -%}
{{ place.name }}
{%- endmacro -%}

{% macro place_links(place) -%}
{% if place.telegram -%}[:simple-telegram:]({{ place.telegram }}) {% endif %} {% if place.untappd -%}[:simple-untappd:]({{ place.untappd }}) {% endif %} {% if place.site -%}[:octicons-link-16:]({{ place.site }}) {% endif %}
{%- endmacro -%}

{% for city, city_places_by_type in beer_places_by_city.items() %}
## {{ city }}

{% for type, places in city_places_by_type.items() %}

**{{ type }}ы**

| Название | Ссылки | Где |
|----------|--------|-----|
{% for place in places -%}
| {{ place_name(place) }} | {{ place_links(place) }} | {{ msk_place_location(place) }} |
{% endfor -%}

{% endfor %}
{% endfor %}
