import Database from 'better-sqlite3'
import { defineEventHandler, readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { url } = body
  
  if (!url) {
    return { error: 'URL is required' }
  }
  
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  const history = db.prepare(`
    SELECT 
      *
    FROM untappd_beer_prices ubp
    WHERE url = ?
    ORDER BY date_parsed DESC, price
  `).all(url)
  
  db.close()
  
  return history
}) 