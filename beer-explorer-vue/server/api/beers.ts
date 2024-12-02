import Database from 'better-sqlite3'
import { defineEventHandler } from 'h3'

export default defineEventHandler(() => {
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  const beers = db.prepare(`
    SELECT b.*, bb.country as country
    FROM beer_my_untappd_beers b
    join beer_breweries bb on b.brewery = bb.name
  `).all()
  
  db.close()
  
  return beers
}) 