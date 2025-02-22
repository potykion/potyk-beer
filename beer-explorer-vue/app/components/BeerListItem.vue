<script lang="ts" setup>

import type {Beer} from "~/logic/beer";

interface Props {
  beer: Beer;
}

const props = defineProps<Props>()
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
      {{ props.beer.brewery }} • {{ beer.rating }} ⭐
    </template>
  </v-list-item>
</template>