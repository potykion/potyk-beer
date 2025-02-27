<script setup lang="ts">
import BeerPricesTable from '~/components/BeerPricesTable.vue'
import {type Beer, compPricePerL} from "~/logic/beer";
import BeerListItem from "~/components/BeerListItem.vue";

interface RawBeerPrice {
  name: string;
  brewery: string;
  venue: string;
  volume: string;
  price: number;
  url: string;
  rate: number;
  abv: number;
  ibu: number;
  style: string;
}

const {data: beerPrices} = await useFetch<RawBeerPrice[]>('/api/beer-prices')

/**
 * Все пивасы с ценами по точкам и объемам
 */
const uniqueBeers = computed<(Beer)[]>(() => {
  const beers = new Map<string, Beer>()

  beerPrices.value?.forEach(raw => {
    const id = `${raw.name}\n${raw.brewery}`

    let beer: Beer;
    if (!beers.has(id)) {
      beer = {
        ...raw,
        venuePrices: [],
      };
      beers.set(id, beer)
    } else {
      beer = beers.get(id)!;
    }

    let venuePrices = beer.venuePrices!.find(venue => venue.venue === raw.venue);
    if (!venuePrices) {
      venuePrices = {
        venue: raw.venue,
        prices: [],
      }
      beer.venuePrices!.push(venuePrices)
    }

    venuePrices.prices.push({
      volume: raw.volume,
      price: raw.price,
    })
  })

  return Array.from(beers.entries()).map(([id, value]) => ({
    id,
    ...value,
  }))
})

const uniqueVenues = computed(() => {
  const venues = new Set<string>()
  beerPrices.value?.forEach(beer => venues.add(beer.venue))
  return Array.from(venues)
})

// Обновляем получение пивоварен с учетом выбранных магазинов
const allBreweryItems = computed(() => {
  const breweriesSet = new Set<string>()

  // Фильтруем пиво по выбранным магазинам
  let filteredPrices = beerPrices.value || []
  if (selectedVenues.value.length > 0) {
    filteredPrices = filteredPrices.filter(beer =>
        selectedVenues.value.includes(beer.venue)
    )
  }

  // Собираем только пивоварни из отфильтрованного списка
  filteredPrices.forEach(beer => breweriesSet.add(beer.brewery))

  const breweries = Array.from(breweriesSet)
  breweries.sort()
  return breweries.map(brewery => ({
    title: brewery,
    value: brewery,
  }))
})

// Обновляем получение стилей с учетом выбранных магазинов
const allStyleItems = computed(() => {
  const allStylesSet = new Set<string>()

  // Фильтруем пиво по выбранным магазинам
  let filteredPrices = beerPrices.value || []
  if (selectedVenues.value.length > 0) {
    filteredPrices = filteredPrices.filter(beer =>
        selectedVenues.value.includes(beer.venue)
    )
  }

  // Собираем стили из отфильтрованного списка
  filteredPrices.forEach(beer => {
    const style = simplifyStyles.value ? beer.style.split(' - ')[0]! : beer.style
    allStylesSet.add(style)
  })

  const allStyles = Array.from(allStylesSet)
  allStyles.sort()
  return allStyles.map(style => ({
    title: style,
    value: style,
  }))
})

// Состояние выбранных пивоварен
const selectedBreweries = ref<string[]>([])

// Добавляем состояние для текстового поиска
const searchQuery = ref('')

// Состояние выбранных магазинов
const selectedVenues = ref<string[]>(uniqueVenues.value.slice(0, 1))

// Состояние чекбокса пересечений
const showIntersectionsOnly = ref(false)

// Обновляем типы подачи
const servingTypes = [
  {title: 'Банки/Бутылки', value: 'packaged'},
  {title: 'Розлив', value: 'draft'},
  {title: 'Сэмплы', value: 'sample'},
]

// Обновляем функцию определения типа подачи
const getServingType = (volume: string): string => {
  const volumeLower = volume.toLowerCase()

  // Проверяем сэмплы
  if (volumeLower.includes('sample') || volumeLower.includes('cl')) {
    return 'sample'
  }

  // Проверяем бутылки/банки
  if (volumeLower.includes('bottle') ||
      volumeLower.includes('can') ||
      volumeLower.includes('btl')) {
    return 'packaged'
  }

  // Все остальное считаем розливом
  return 'draft'
}

// Обновляем начальное состояние выбранных типов подачи
const selectedServingTypes = ref(['packaged', 'draft',])

const sortByOptions = [
  {title: 'По алкоголю', value: 'abv'},
  {title: 'По цене', value: 'price'},
  {title: 'По цене за литр', value: 'pricePerL'},
  {title: 'По названию', value: 'name'},
]

const sortBy = ref<'abv' | 'price' | 'pricePerL' | 'name' | null>('pricePerL')

// Обновляем список отображаемых магазинов
const displayedVenues = computed(() => {
  if (selectedVenues.value.length === 0) {
    return uniqueVenues.value
  }
  return selectedVenues.value
})

// Добавляем состояние для выбранных стилей
const selectedStyles = ref<string[]>([])

// Добавляем состояние для упрощения стилей
const simplifyStyles = ref(true)

// Обновляем фильтрацию с учетом стилей
const filteredBeers = computed(() => {
  let filtered = uniqueBeers.value.map(beer => ({
    ...beer,
    style: simplifyStyles.value ? beer.style.split(' - ')[0]! : beer.style
  }))

  if (hideTried.value) {
    filtered = filtered.filter(f => !f.tried)
  }



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

  // Фильтрация по выбранным магазинам и типу подачи
  if (selectedVenues.value.length > 0 || selectedServingTypes.value.length < servingTypes.length) {
    filtered = filtered.filter(beer => {
      // Получаем все цены для данного пива
      const beerPricesForVenues = beer.venuePrices!.flatMap(venuePrices => venuePrices.prices.map(price => ({
        ...price,
        venue: venuePrices.venue
      })));
      // Проверяем наличие выбранных типов подачи
      const hasSelectedServingType = beerPricesForVenues?.some(price =>
          selectedServingTypes.value.includes(getServingType(price.volume))
      )

      if (!hasSelectedServingType) {
        return false
      }

      if (selectedVenues.value.length === 0) {
        return true
      }

      if (showIntersectionsOnly.value) {
        return selectedVenues.value.every(venue => {
          return beerPricesForVenues?.some(price =>
              price.venue === venue &&
              selectedServingTypes.value.includes(getServingType(price.volume))
          )
        })
      } else {
        return selectedVenues.value.some(venue => {
          return beerPricesForVenues?.some(price =>
              price.venue === venue &&
              selectedServingTypes.value.includes(getServingType(price.volume))
          )
        })
      }
    })
        .map(beer => ({
          ...beer, venuePrices: beer.venuePrices!

              // Фильтруем только выбранные магазины
              .filter(venuePrices => selectedVenues.value.length === 0 || selectedVenues.value.includes(venuePrices.venue))

              // Фильтруем только выбранные типы подачи
              .map(venuePrices => ({
                    ...venuePrices,
                    prices: venuePrices.prices.filter(price => selectedServingTypes.value.includes(getServingType(price.volume))),
                  })
              )
        }))
  }

  // Фильтрация по выбранным стилям
  if (selectedStyles.value.length) {
    filtered = filtered.filter(beer =>
        selectedStyles.value.includes(beer.style)
    )
  }

   if (sortBy.value) {
    if (sortBy.value === "abv") {
      filtered.sort((a, b) => a.abv - b.abv)
    } else if (sortBy.value === "name") {
      filtered.sort((a, b) => a.name.localeCompare(b.name))
    } else if (sortBy.value === "price") {
      filtered.sort((a, b) => {
        const aMinPrice = Math.min(...a.venuePrices!.flatMap(vp => vp.prices).flatMap(p => p.price))
        const bMinPrice = Math.min(...b.venuePrices!.flatMap(vp => vp.prices).flatMap(p => p.price))

        return aMinPrice - bMinPrice;
      })
    } else if (sortBy.value === "pricePerL") {
      filtered.sort((a, b) => {

        const aMinPricePerL = Math.min(...a.venuePrices!.flatMap(vp => vp.prices).flatMap(p => compPricePerL(p.price, p.volume)))
        const bMinPricePerL = Math.min(...b.venuePrices!.flatMap(vp => vp.prices).flatMap(p => compPricePerL(p.price, p.volume)))

        return aMinPricePerL - bMinPricePerL;
      })
    }
  }

  return filtered
})

// Добавляем состояние для режима отображения
const displayMode = ref<'table' | 'list'>('list')

const hideTried = ref(true);
</script>

<template>
  <v-container fluid>
    <div class="search-container">
      <v-row>
        <v-col cols="12" class="d-flex align-center">
          <v-text-field
              v-model="searchQuery"
              label="Поиск по названию или пивоварне"
              variant="outlined"
              clearable
              density="comfortable"
              class="flex-grow-1"
              hide-details
          />
          <v-btn-toggle
              v-model="displayMode"
              mandatory
              class="ms-4"
          >
            <v-btn value="table" icon="mdi-table"/>
            <v-btn value="list" icon="mdi-format-list-bulleted"/>
          </v-btn-toggle>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4">
          <div>
            <v-autocomplete
                v-model="selectedVenues"
                :items="uniqueVenues"
                chips
                label="Выберите магазины"
                multiple
                variant="outlined"
                hide-details
                clearable
            />
            <v-checkbox
                v-if="selectedVenues.length > 1"
                v-model="showIntersectionsOnly"
                label="Только пересечения"
                :disabled="selectedVenues.length <= 1"
                density="comfortable"
                class="mt-2"
            />
          </div>
        </v-col>

        <v-col cols="4">
          <v-autocomplete
              v-model="selectedBreweries"
              :items="allBreweryItems"
              chips
              label="Выберите пивоварни"
              multiple
              variant="outlined"
              clearable
          />
        </v-col>

        <v-col cols="4">
          <v-autocomplete
              v-model="selectedStyles"
              :items="allStyleItems"
              chips
              label="Выберите стили"
              multiple
              variant="outlined"
              clearable
              hide-details
          />
          <v-checkbox
              v-model="simplifyStyles"
              label='Упрощенные стили ("Barleywine - American" → "Barleywine")'
              density="comfortable"
              class="mt-2"
              hide-details
          />
        </v-col>

        <v-col cols="4">
          <v-select
              v-model="selectedServingTypes"
              :items="servingTypes"
              chips
              label="Тип подачи"
              multiple
              variant="outlined"
          />
        </v-col>

        <v-col cols="4">
          <v-select
              v-model="sortBy"
              :items="sortByOptions"
              label="Сортировка"
              variant="outlined"
          />
        </v-col>

        <v-col cols="4">
          <v-checkbox
              v-model="hideTried"
              label='Скрыть попробованные'
          />
        </v-col>
      </v-row>
    </div>

    <template v-if="displayMode === 'table'">
      <BeerPricesTable
          :filtered-beers="filteredBeers"
          :displayed-venues="displayedVenues"
      />
    </template>
    <template v-else>
      <v-row>
        <v-col cols="12" sm="6">
          <v-list>
            <BeerListItem
                v-for="beer in filteredBeers.slice(0, Math.ceil(filteredBeers.length / 2))"
                :key="beer.id"
                :beer="beer"
            />
          </v-list>
        </v-col>
        <v-col cols="12" sm="6">
          <v-list>
            <BeerListItem
                v-for="beer in filteredBeers.slice(Math.ceil(filteredBeers.length / 2))"
                :key="beer.id"
                :beer="beer"
            />
          </v-list>

        </v-col>
      </v-row>


    </template>
  </v-container>
</template>

<style scoped>
/*
.prices-container {
  padding: 1rem;
  overflow-x: auto;
  position: relative;
  max-height: calc(100vh - 2rem);
}

 */

.search-container {
  margin-bottom: 1rem;
  background-color: white;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}
</style>