select style, count(style)
from beru_vyh_beers
where price < 400
group by style
order by count(style) desc

select * from beru_vyh_beers
where
--     style ='Saison'
    brewery ='Eibau'

-- and price < 400
and brewery != 'Hophead' and brewery != 'Magic Mess'
order by price desc

select brewery, count(brewery) from beru_vyh_beers group by brewery order by count()desc

SELECT brewery,
       COUNT(brewery) as Count,
       (SELECT GROUP_CONCAT(title)
        FROM (SELECT title
              FROM beru_vyh_beers
              WHERE brewery = main.brewery
              ORDER BY title
              LIMIT 5)) as Titles
FROM beru_vyh_beers as main
GROUP BY brewery
ORDER BY Count DESC

delete from beru_vyh_beers


WITH numbered_rows AS (
  SELECT
    brewery,
    title,
    COUNT(*) OVER (PARTITION BY brewery) as Count,
    ROW_NUMBER() OVER (PARTITION BY brewery ORDER BY title) as rn
  FROM
    beru_vyh_beers
)
SELECT brewery, Count, title
FROM numbered_rows
WHERE rn <= 5
ORDER BY Count DESC, brewery, rn;
