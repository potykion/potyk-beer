<script setup lang="ts">
import type {Beer} from "~/logic/beer";

defineProps<{
  filteredBeers: Beer[]
  displayedVenues: string[]
}>()


function getPricesForBeerAndVenue(beer: Beer, venue: string): string {
  return (beer.venuePrices?.find(venuePrices => venuePrices.venue === venue)?.prices || [])
      .map(price => `${price.volume} - ${price.price} ₽`).join('<br>')
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
    <tr v-for="beer in filteredBeers" :key="beer.id">
      <td class="beer-name">
        <a :href="beer.url" target="_blank">
          <strong>{{ beer.name }}</strong><br>
          {{ beer.brewery }}
        </a>
      </td>
      <td v-for="venue in displayedVenues" :key="venue" v-html="getPricesForBeerAndVenue(beer, venue)"></td>
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