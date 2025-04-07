import Database from 'better-sqlite3'
import { defineEventHandler } from 'h3'

export default defineEventHandler(() => {
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  const prices = db.prepare(`
    SELECT 
      *, (select 1 from beer_my_untappd_beers bmub where bmub.url = ubp.url) as tried
    FROM untappd_beer_prices ubp
    where price > 0 and date_parsed = (select max(date_parsed) from untappd_beer_prices)
    ORDER BY price

    
    
  `).all()
  
  db.close()
  
  return prices
}) 