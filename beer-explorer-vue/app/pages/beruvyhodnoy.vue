<script setup lang="ts">
import { ref, computed } from 'vue'

// Определяем типы данных
interface Beer {
  name: string
  country: string
  style: string
  density: string
  alcohol: string
  brewery: string
}

interface Shop {
  shop: string
}

interface PriceData {
  name: string
  shop: string
  price: string
}

interface BeerData {
  beers: Beer[]
  shops: Shop[]
  prices: PriceData[]
}

// Получаем данные с сервера
const { data: beerData } = await useFetch<BeerData>('/api/beruvyhodnoy-beers')

// Рассчитываем данные для таблицы
const shops = computed(() => beerData.value?.shops || [])
const beers = computed(() => beerData.value?.beers || [])
const prices = computed(() => {
  const priceMap = new Map()
  
  if (beerData.value?.prices) {
    beerData.value.prices.forEach((item: PriceData) => {
      const key = `${item.name}|${item.shop}`
      priceMap.set(key, item.price)
    })
  }
  
  return priceMap
})

// Получение цены для конкретного пива в конкретном магазине
function getPrice(beer: Beer, shop: Shop) {
  const key = `${beer.name}|${shop.shop}`
  return prices.value.get(key) || null
}
</script>

<template>
  <div class="beruvyhodnoy-container">
    <h1>Цены на пиво в "Беру Выходной"</h1>
    
    <div class="table-container">
      <table class="beer-table">
        <thead>
          <tr>
            <th class="beer-column">Пиво</th>
            <th v-for="shop in shops" :key="shop.shop" class="shop-column">
              {{ shop.shop }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="beer in beers" :key="beer.name">
            <td class="beer-info">
              <div class="beer-name">{{ beer.name }}</div>
              <div class="beer-details">
                {{ beer.country }}, {{ beer.style }}, 
                <span v-if="beer.density && beer.density !== '0'">{{ beer.density }}°P,</span>
                {{ beer.alcohol }}%, {{ beer.brewery }}
              </div>
            </td>
            <td v-for="shop in shops" :key="`${beer.name}-${shop.shop}`" class="price-cell">
              <div v-if="getPrice(beer, shop)" class="price">
                {{ getPrice(beer, shop) }}₽
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.beruvyhodnoy-container {
  padding: 20px;
  max-width: 100%;
  overflow-x: auto;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
}

.table-container {
  overflow-x: auto;
  width: 100%;
}

.beer-table {
  border-collapse: collapse;
  width: 100%;
}

.beer-table th, .beer-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.beer-table thead {
  background-color: #f2f2f2;
  position: sticky;
  top: 0;
}

.beer-column {
  min-width: 300px;
  text-align: left;
}

.shop-column {
  min-width: 120px;
  text-align: center;
}

.beer-name {
  font-weight: bold;
  margin-bottom: 4px;
}

.beer-details {
  font-size: 0.8em;
  color: #666;
}

.price-cell {
  text-align: center;
}

.price {
  font-weight: bold;
}
</style>