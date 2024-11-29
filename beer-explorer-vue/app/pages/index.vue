<script lang="ts" setup>
interface Beer {
  brewery: string
  name: string
  rating: number
  url: string
}

const {data: beers} = await useFetch<Beer[]>('/api/beers')

const groupers = [
  {
    title: 'Пивоварня',
    value: 'brewery',
  }
]

const selectedGroups = ref([])

// Функция для группировки пива
const groupedBeers = computed(() => {
  if (!beers.value || selectedGroups.value.length === 0) {
    return { ungrouped: beers.value || [] }
  }

  const groupBy = selectedGroups.value[0] // Берем первую выбранную группировку
  
  return beers.value.reduce((acc, beer) => {
    const key = beer[groupBy]
    if (!acc[key]) {
      acc[key] = []
    }
    acc[key].push(beer)
    return acc
  }, {})
})
</script>

<template>
  <v-container>
    <h1>Пивко</h1>

    <v-row class="pt-5">
      <v-col>
        <v-select
            v-model="selectedGroups"
            chips
            label="Группировка"
            :items="groupers"
            multiple
            variant="outlined"
            density="compact"
        ></v-select>
      </v-col>
      <v-col>
        <v-select
            chips
            label="Сортировка"
            :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            multiple
            variant="outlined"
            density="compact"
        ></v-select>
      </v-col>
    </v-row>

    <div>
      <template v-for="(beersInGroup, groupName) in groupedBeers" :key="groupName">
        <v-list-subheader v-if="selectedGroups.length > 0">
          {{ groupName }}
        </v-list-subheader>
        
        <v-list density="compact">
          <v-list-item
              v-for="beer in beersInGroup"
              :key="`${beer.brewery}-${beer.name}`"
              :href="beer.url"
              target="_blank"
          >
            <v-list-item-title>
              {{ beer.brewery }} — {{ beer.name }} ({{ beer.rating }})
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </div>
  </v-container>
</template>

