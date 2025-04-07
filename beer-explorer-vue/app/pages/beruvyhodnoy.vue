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

// Фильтры
const selectedCountries = ref<string[]>(["Россия"])
const selectedBreweries = ref<string[]>([])
const selectedStyles = ref<string[]>([])

// Получаем уникальные страны
const countries = computed(() => {
  const uniqueCountries = new Set<string>()
  beers.value.forEach(beer => uniqueCountries.add(beer.country))
  return Array.from(uniqueCountries).sort().map(country => ({
    title: country,
    value: country
  }))
})

// Получаем уникальные пивоварни с учетом выбранных стран
const breweries = computed(() => {
  const uniqueBreweries = new Set<string>()
  
  // Фильтруем пиво по выбранным странам (если они выбраны)
  let filteredBeers = beers.value
  if (selectedCountries.value.length > 0) {
    filteredBeers = filteredBeers.filter(beer => selectedCountries.value.includes(beer.country))
  }
  
  // Собираем пивоварни из отфильтрованного списка
  filteredBeers.forEach(beer => uniqueBreweries.add(beer.brewery))
  
  return Array.from(uniqueBreweries).sort().map(brewery => ({
    title: brewery,
    value: brewery
  }))
})

// Получаем уникальные стили с учетом выбранных стран и пивоварен
const styles = computed(() => {
  const uniqueStyles = new Set<string>()
  
  // Фильтруем пиво по выбранным странам и пивоварням (если они выбраны)
  let filteredBeers = beers.value
  
  if (selectedCountries.value.length > 0) {
    filteredBeers = filteredBeers.filter(beer => selectedCountries.value.includes(beer.country))
  }
  
  if (selectedBreweries.value.length > 0) {
    filteredBeers = filteredBeers.filter(beer => selectedBreweries.value.includes(beer.brewery))
  }
  
  // Собираем стили из отфильтрованного списка
  filteredBeers.forEach(beer => uniqueStyles.add(beer.style))
  
  return Array.from(uniqueStyles).sort().map(style => ({
    title: style,
    value: style
  }))
})

// Фильтрованный список пива
const filteredBeers = computed(() => {
  let filtered = beers.value
  
  if (selectedCountries.value.length > 0) {
    filtered = filtered.filter(beer => selectedCountries.value.includes(beer.country))
  }
  
  if (selectedBreweries.value.length > 0) {
    filtered = filtered.filter(beer => selectedBreweries.value.includes(beer.brewery))
  }
  
  if (selectedStyles.value.length > 0) {
    filtered = filtered.filter(beer => selectedStyles.value.includes(beer.style))
  }
  
  return filtered
})

// Состояние для управления отображением фильтров
const showFilters = ref(false)
</script>

<template>
  <div class="beruvyhodnoy-container">
    <h1>Цены на пиво в "Беру Выходной"</h1>
    
    <!-- Фильтры -->
    <div class="filters-container">
      <v-card>
        <v-card-item @click="showFilters = !showFilters" style="cursor: pointer">
          <v-card-title>Фильтры</v-card-title>
          <template v-slot:append>
            <v-btn flat icon>
              <v-icon v-if="showFilters">mdi-menu-up</v-icon>
              <v-icon v-else>mdi-menu-down</v-icon>
            </v-btn>
          </template>
        </v-card-item>
        
        <v-expand-transition>
          <div v-if="showFilters">
            <v-card-text>
              <v-row>
                <v-col cols="4">
                  <v-autocomplete
                    v-model="selectedCountries" 
                    :items="countries" 
                    chips 
                    label="Страна" 
                    multiple 
                    variant="outlined"
                    clearable
                  />
                </v-col>
                
                <v-col cols="4">
                  <v-autocomplete
                    v-model="selectedBreweries" 
                    :items="breweries" 
                    chips 
                    label="Пивоварня" 
                    multiple 
                    variant="outlined"
                    clearable
                  />
                </v-col>
                
                <v-col cols="4">
                  <v-autocomplete
                    v-model="selectedStyles" 
                    :items="styles" 
                    chips 
                    label="Стиль" 
                    multiple 
                    variant="outlined"
                    clearable
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>
    </div>
    
    <!-- Таблица с ценами -->
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
          <tr v-for="beer in filteredBeers" :key="beer.name">
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

.filters-container {
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto;
  width: 100%;
  margin-top: 20px;
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