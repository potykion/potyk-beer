<script lang="ts" setup>

import type {Beer} from "~/logic/beer";

interface Props {
  beer: Beer;
}

const props = defineProps<Props>()

// array of stars
const stars = computed(() => Array.from({length: Math.round(props.beer.rate)}, (_, __) => "⭐").join(""))


</script>

<template>
  <v-list-item
      :href="beer.url"
      target="_blank"
  >
    <template v-slot:title>
      <div>
        <span class="font-weight-bold text-body-1">{{ beer.name }}</span>&nbsp;
        <span class="text-body-2 font-italic">{{ beer.style }}</span>
      </div>
    </template>

    <template v-slot:subtitle>
      {{ beer.abv }}% ABV • {{ beer.ibu }} IBU • {{ props.beer.brewery }} • {{ stars }} ({{ beer.rate }})
    </template>

    <template v-for="venue in props.beer.venuePrices" :key="venue.venue">
      <template v-if="venue.prices.length > 0">
        <div class="text-body-2">
          <div class="font-weight-bold">{{ venue.venue }}</div>
          <div v-for="price in venue.prices" :key="price.volume">
            {{ price.volume }} - {{ price.price }} ₽
          </div>
        </div>
      </template>
    </template>

  </v-list-item>
</template>