import Database from 'better-sqlite3'
import { defineEventHandler } from 'h3'

export default defineEventHandler(() => {
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  const prices = db.prepare(`
    SELECT 
      *
    FROM untappd_beer_prices
    where price > 0
    ORDER BY price
    
  `).all()
  
  db.close()
  
  return prices
}) 