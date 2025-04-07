import Database from 'better-sqlite3'
import { defineEventHandler } from 'h3'

export default defineEventHandler(() => {
  const db = new Database('C:\\Users\\admin\\PycharmProjects\\beer-board\\beer.db')
  
  // Получаем список всех пив с уникальными названиями
  const beers = db.prepare(`
    SELECT 
      name,
      country,
      style,
      density,
      alcohol,
      brewery
    FROM beruvyhodnoy_beers
    WHERE date = (SELECT MAX(date) FROM beruvyhodnoy_beers)
    GROUP BY name
    ORDER BY name
  `).all()
  
  // Получаем список всех магазинов
  const shops = db.prepare(`
    SELECT DISTINCT shop
    FROM beruvyhodnoy_beers
    WHERE date = (SELECT MAX(date) FROM beruvyhodnoy_beers)
    ORDER BY shop
  `).all()
  
  // Получаем цены для каждого пива в каждом магазине
  const prices = db.prepare(`
    SELECT 
      name,
      shop,
      price
    FROM beruvyhodnoy_beers
    WHERE date = (SELECT MAX(date) FROM beruvyhodnoy_beers)
  `).all()
  
  // Преобразуем данные в формат для удобного отображения
  const result = {
    beers,
    shops,
    prices
  }
  
  db.close()
  
  return result
}) 