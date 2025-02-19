<script setup lang="ts">
interface BeerPrice {
  name: string
  brewery: string
  venue: string
  volume: string
  price: number
  url: string
}

const { data: beerPrices } = await useFetch<BeerPrice[]>('/api/beer-prices')

// Подготовка данных для таблицы
const uniqueBeers = computed(() => {
  const beers = new Map<string, { name: string, brewery: string, url: string, displayName: string }>()
  
  beerPrices.value?.forEach(beer => {
    const key = `${beer.name}\n${beer.brewery}`
    if (!beers.has(key)) {
      beers.set(key, { 
        name: beer.name, 
        brewery: beer.brewery, 
        url: beer.url,
        displayName: `<strong>${beer.name}</strong>\n${beer.brewery}`
      })
    }
  })
  
  return Array.from(beers.entries()).map(([key, value]) => ({
    key,
    ...value
  }))
})

const uniqueVenues = computed(() => {
  const venues = new Set<string>()
  beerPrices.value?.forEach(beer => venues.add(beer.venue))
  return Array.from(venues)
})

const getPricesForBeerAndVenue = (beerKey: string, venue: string) => {
  const [name, brewery] = beerKey.split('\n')
  return beerPrices.value
    ?.filter(beer => 
      beer.name === name && 
      beer.brewery === brewery && 
      beer.venue === venue
    )
    .map(beer => `${beer.volume} - ${beer.price}₽`)
    .join('<br>') || ''
}
</script>

<template>
  <div class="prices-container">
    <table class="prices-table">
      <thead>
        <tr>
          <th>Пиво</th>
          <th v-for="venue in uniqueVenues" :key="venue">{{ venue }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="beer in uniqueBeers" :key="beer.key">
          <td class="beer-name">
            <a :href="beer.url" target="_blank" v-html="beer.displayName"></a>
          </td>
          <td v-for="venue in uniqueVenues" :key="venue" v-html="getPricesForBeerAndVenue(beer.key, venue)">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.prices-container {
  padding: 1rem;
  overflow-x: auto;
  position: relative;
  max-height: calc(100vh - 2rem);  /* Ограничиваем высоту контейнера */
}

.prices-table {
  width: 100%;
  border-collapse: separate;  /* Меняем на separate для работы position: sticky */
  border-spacing: 0;  /* Убираем отступы между ячейками */
  min-width: 800px;
  table-layout: fixed;
}

.prices-table th,
.prices-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  width: auto;
  min-width: 120px;
}

.prices-table th {
  background-color: #f2f2f2;
  position: sticky;  /* Делаем заголовки фиксированными */
  top: 0;
  z-index: 1;  /* Чтобы заголовки были поверх содержимого при прокрутке */
  /* Добавляем тень для визуального отделения */
  box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.1);
}

.beer-name {
  white-space: pre-line;
  width: 200px;
}

.beer-name a {
  color: #2c3e50;
  text-decoration: none;
}

.beer-name a:hover {
  text-decoration: underline;
  color: #42b883;
}

.prices-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.prices-table tr:hover {
  background-color: #f5f5f5;
}
</style>