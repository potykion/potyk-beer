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

// Получаем уникальные пивоварни
const uniqueBreweries = computed(() => {
  const breweries = new Set<string>()
  beerPrices.value?.forEach(beer => breweries.add(beer.brewery))
  return Array.from(breweries).map(brewery => ({
    title: brewery,
    value: brewery,
  }))
})

// Состояние выбранных пивоварен
const selectedBreweries = ref<string[]>([])

// Добавляем состояние для текстового поиска
const searchQuery = ref('')

// Состояние выбранных магазинов
const selectedVenues = ref<string[]>([])

// Состояние чекбокса пересечений
const showIntersectionsOnly = ref(false)

// Обновляем список отображаемых магазинов
const displayedVenues = computed(() => {
  if (selectedVenues.value.length === 0) {
    return uniqueVenues.value
  }
  return selectedVenues.value
})

// Обновляем фильтрацию с учетом магазинов и пересечений
const filteredBeers = computed(() => {
  let filtered = uniqueBeers.value

  // Фильтрация по выбранным пивоварням
  if (selectedBreweries.value.length) {
    filtered = filtered.filter(beer => 
      selectedBreweries.value.includes(beer.brewery)
    )
  }

  // Фильтрация по текстовому поиску
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(beer =>
      beer.name.toLowerCase().includes(query) ||
      beer.brewery.toLowerCase().includes(query)
    )
  }

  // Фильтрация по выбранным магазинам
  if (selectedVenues.value.length > 0) {
    filtered = filtered.filter(beer => {
      const [name, brewery] = beer.key.split('\n')
      
      if (showIntersectionsOnly.value) {
        // Показывать только пиво, которое есть во всех выбранных магазинах
        return selectedVenues.value.every(venue => {
          return beerPrices.value?.some(price => 
            price.name === name && 
            price.brewery === brewery && 
            price.venue === venue
          )
        })
      } else {
        // Показывать пиво, которое есть хотя бы в одном из выбранных магазинов
        return selectedVenues.value.some(venue => {
          return beerPrices.value?.some(price => 
            price.name === name && 
            price.brewery === brewery && 
            price.venue === venue
          )
        })
      }
    })
  }

  return filtered
})
</script>

<template>
  <div class="prices-container">
    <div class="search-container">
      <div class="search-controls">
        <v-text-field
          v-model="searchQuery"
          label="Поиск по названию или пивоварне"
          variant="outlined"
          class="search-field"
          clearable
          density="comfortable"
        />
        <v-autocomplete
          v-model="selectedBreweries"
          :items="uniqueBreweries"
          chips
          label="Выберите пивоварни"
          multiple
          variant="outlined"
          class="brewery-select"
        />
      </div>
      <div class="venue-controls">
        <v-autocomplete
          v-model="selectedVenues"
          :items="uniqueVenues"
          chips
          label="Выберите магазины"
          multiple
          variant="outlined"
          class="venue-select"
        />
        <v-checkbox
          v-model="showIntersectionsOnly"
          label="Только пересечения"
          :disabled="selectedVenues.length <= 1"
          density="comfortable"
        />
      </div>
    </div>
    
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
  </div>
</template>

<style scoped>
.prices-container {
  padding: 1rem;
  overflow-x: auto;
  position: relative;
  max-height: calc(100vh - 2rem);  /* Ограничиваем высоту контейнера */
}

.search-container {
  margin-bottom: 1rem;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 2;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.search-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-field {
  max-width: 300px;
  flex: 1;
}

.brewery-select {
  max-width: 600px;
  flex: 2;
}

.venue-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 1rem;
}

.venue-select {
  max-width: 600px;
  flex: 1;
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