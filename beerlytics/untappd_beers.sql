select title, style, abv, rating, rating_amount, link
from untappd_beers
where rating_amount > 2000
order by rating desc

select style, count(style)
from untappd_beers
group by style
order by count(style) desc

select title, style, abv, rating, rating_amount, link
    from untappd_beers
where style = 'IPA - American'
and rating_amount > 2000
order by rating_amount desc, rating desc