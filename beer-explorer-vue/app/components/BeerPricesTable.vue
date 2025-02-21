<script setup lang="ts">
interface BeerPrice {
  name: string
  brewery: string
  venue: string
  volume: string
  price: number
  url: string
}

interface Beer {
  key: string
  name: string
  brewery: string
  url: string
  displayName: string
}

const props = defineProps<{
  beerPrices: BeerPrice[] | null
  filteredBeers: Beer[]
  displayedVenues: string[]
  selectedServingTypes: string[]
}>()

// Функция получения цен с учетом типа подачи
const getPricesForBeerAndVenue = (beerKey: string, venue: string) => {
  const [name, brewery] = beerKey.split('\n')
  return props.beerPrices
    ?.filter(beer => 
      beer.name === name && 
      beer.brewery === brewery && 
      beer.venue === venue &&
      props.selectedServingTypes.includes(getServingType(beer.volume))
    )
    .map(beer => `${beer.volume} - ${beer.price}₽`)
    .join('<br>') || ''
}

// Функция определения типа подачи
const getServingType = (volume: string): string => {
  const volumeLower = volume.toLowerCase()
  
  if (volumeLower.includes('sample') || volumeLower.includes('cl')) {
    return 'sample'
  }
  
  if (volumeLower.includes('bottle') || 
      volumeLower.includes('can') || 
      volumeLower.includes('btl')) {
    return 'packaged'
  }
  
  return 'draft'
}
</script>

<template>
  <table class="prices-table">
    <thead>
      <tr>
        <th>Пиво</th>
        <th v-for="venue in displayedVenues" :key="venue">{{ venue }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="beer in filteredBeers" :key="beer.key">
        <td class="beer-name">
          <a :href="beer.url" target="_blank" v-html="beer.displayName"></a>
        </td>
        <td v-for="venue in displayedVenues" :key="venue" v-html="getPricesForBeerAndVenue(beer.key, venue)">
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.prices-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
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
  position: sticky;
  top: 0;
  z-index: 1;
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