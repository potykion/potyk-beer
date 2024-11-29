<script lang="ts" setup>
interface Beer {
  brewery: string
  name: string
  rating: number
  url: string
  style: string
}


interface Props {
  beer: Beer;
}

const props = defineProps<Props>()

</script>

<template>
  <v-list-item

      :href="beer.url"
      :title='`<span class="font-weight-bold text-body-1">${beer.name}</span> <span class="text-body-2 font-italic">${beer.style}</span>`'
      target="_blank"
      :subtitle='`${props.beer.brewery} • ${beer.rating} ⭐`'
  >

    <template v-slot:title="{ title }">
      <div v-html="title"></div>
    </template>
  </v-list-item>
</template> 