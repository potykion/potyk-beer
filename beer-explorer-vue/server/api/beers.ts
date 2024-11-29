import Database from 'better-sqlite3'
import { defineEventHandler } from 'h3'

export default defineEventHandler(() => {
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  const beers = db.prepare(`
    SELECT * 
    FROM beer_my_untappd_beers
  `).all()
  
  db.close()
  
  return beers
}) 