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



</script>

<template>
  <v-container>
    <h1>Пивко</h1>

    <v-row class="pt-5">
      <v-col>
        <v-select
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


    <div >
      <v-list density="compact">
        <v-list-item
            v-for="beer in beers"
            :key="`${beer.brewery}-${beer.name}`"
            :href="beer.url"
            target="_blank"
        >
          <v-list-item-title>
            {{ beer.brewery }} — {{ beer.name }} ({{ beer.rating }})
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </div>
  </v-container>
</template>

