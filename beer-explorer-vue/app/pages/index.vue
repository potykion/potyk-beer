<script lang="ts" setup>
interface Beer {
  brewery: string
  name: string
  rating: number
  url: string
  style: string
}

const {data: beers} = await useFetch<Beer[]>('/api/beers')

const groupers = [
  {
    title: 'Пивоварня',
    value: 'brewery',
  },
  {
    title: 'Стиль',
    value: 'style',
  },
]

const selectedGroups = ref<string[]>([])

type GroupedBeers = {
  [key: string]: Beer[] | {
    [key: string]: Beer[]
  }
}

// Функция для группировки пива
const groupedBeers = computed(() => {
  if (!beers.value || selectedGroups.value.length === 0) {
    return { ungrouped: beers.value || [] }
  }

  const result: GroupedBeers = {}
  
  // Ограничиваем количество группировок до 2
  const activeGroups = selectedGroups.value.slice(0, 2)
  
  beers.value.forEach((beer) => {
    const firstKey = beer[activeGroups[0] as keyof Beer] as string
    
    if (activeGroups.length === 1) {
      if (!result[firstKey]) {
        result[firstKey] = []
      }
      (result[firstKey] as Beer[]).push(beer)
    } else {
      if (!result[firstKey]) {
        result[firstKey] = {}
      }
      
      const secondKey = beer[activeGroups[1] as keyof Beer] as string
      const subGroup = result[firstKey] as { [key: string]: Beer[] }
      
      if (!subGroup[secondKey]) {
        subGroup[secondKey] = []
      }
      subGroup[secondKey].push(beer)
    }
  })
  
  return result
})

// Проверка является ли группа массивом пива
const isBeersArray = (value: Beer[] | { [key: string]: Beer[] }): value is Beer[] => {
  return Array.isArray(value)
}
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
            :rules="[v => v.length <= 2 || 'Максимум 2 группировки']"
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
      <template v-for="(groupContent, groupName) in groupedBeers" :key="groupName">
        <!-- Заголовок первого уровня -->
        <v-list-subheader v-if="selectedGroups.length > 0 && groupName !== 'ungrouped'">
          {{ groupName }}
        </v-list-subheader>
        
        <!-- Если это финальная группа с пивом -->
        <template v-if="isBeersArray(groupContent)">
          <v-list density="compact">
            <v-list-item
                v-for="beer in groupContent"
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
        
        <!-- Если это подгруппа -->
        <template v-else>
          <div class="pl-4">
            <template v-for="(subGroupBeers, subGroupName) in groupContent" :key="subGroupName">
              <v-list-subheader>{{ subGroupName }}</v-list-subheader>
              <v-list density="compact">
                <v-list-item
                    v-for="beer in subGroupBeers"
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
        </template>
      </template>
    </div>
  </v-container>
</template>

