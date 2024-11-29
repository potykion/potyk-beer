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
    title: 'Стиль',
    value: 'style',
  },
  {
    title: 'Пивоварня',
    value: 'brewery',
  },

]

const selectedGroups = ref<string[]>(['style'])

type GroupedBeers = {
  [key: string]: Beer[] | {
    [key: string]: Beer[]
  }
}

// Функция сортировки пива внутри группы
const sortBeers = (beers: Beer[]): Beer[] => {
  if (!selectedInsideGroupSorters.value.length) return beers
  
  const sortType = selectedInsideGroupSorters.value[0]
  
  return [...beers].sort((a, b) => {
    if (sortType === 'rating') {
      return b.rating - a.rating // По убыванию рейтинга
    } else {
      return a.name.localeCompare(b.name) // По названию
    }
  })
}

// Обновляем функцию сортировки групп
const sortGroups = (groups: GroupedBeers): GroupedBeers => {
  if (!selectedGroupSorters.value.length && !selectedInsideGroupSorters.value.length) return groups
  
  const entries = Object.entries(groups)
  if (entries.length <= 1) return groups
  
  const sortType = selectedGroupSorters.value[0]
  
  // Сортировка групп первого уровня
  const sortedEntries = entries.sort((a, b) => {
    if (a[0] === 'ungrouped') return 1
    if (b[0] === 'ungrouped') return -1
    
    if (sortType === 'amount') {
      const aSize = isBeersArray(a[1]) ? a[1].length : Object.values(a[1]).reduce((sum, arr) => sum + arr.length, 0)
      const bSize = isBeersArray(b[1]) ? b[1].length : Object.values(b[1]).reduce((sum, arr) => sum + arr.length, 0)
      return bSize - aSize
    } else {
      return a[0].localeCompare(b[0])
    }
  })
  
  // Сортировка подгрупп и их содержимого
  const sortedGroups = sortedEntries.map(([key, value]) => {
    if (isBeersArray(value)) {
      // Если это конечная группа - сортируем пиво
      return [key, sortBeers(value)]
    } else {
      // Если это группа с подгруппами
      const subEntries = Object.entries(value)
      const sortedSubEntries = subEntries.sort((a, b) => {
        if (sortType === 'amount') {
          return b[1].length - a[1].length
        } else {
          return a[0].localeCompare(b[0])
        }
      }).map(([subKey, subValue]) => {
        // Сортируем пиво внутри каждой подгруппы
        return [subKey, sortBeers(subValue)]
      })
      return [key, Object.fromEntries(sortedSubEntries)]
    }
  })
  
  return Object.fromEntries(sortedGroups)
}

const simplifyStyles = ref(false)

// Создаем вычисляемое свойство для обработанного списка пива
const processedBeers = computed(() => {
  if (!beers.value) return []
  
  return beers.value.map(beer => ({
    ...beer,
    style: simplifyStyles.value ? beer.style.split(' - ')[0] : beer.style
  }))
})

// Обновляем вычисляемое свойство groupedBeers, 
// заменяем использование beers.value на processedBeers.value
const groupedBeers = computed(() => {
  if (!processedBeers.value || selectedGroups.value.length === 0) {
    return {ungrouped: processedBeers.value || []}
  }

  const result: GroupedBeers = {}
  const activeGroups = selectedGroups.value.slice(0, 2)

  processedBeers.value.forEach((beer) => {
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

  return sortGroups(result)
})

// Проверка является ли группа массивом пива
const isBeersArray = (value: Beer[] | { [key: string]: Beer[] }): value is Beer[] => {
  return Array.isArray(value)
}


const groupSorters = [
  {
    title: "По количеству",
    value: "amount",
  },
  {
    title: "По названию",
    value: "name",
  },

];

const selectedGroupSorters = ref<string[]>(["name"])

const insideGroupSorters = [
  {
    title: "По рейтингу",
    value: "rating",
  },
  {
    title: "По названию",
    value: "name",
  }
];

const selectedInsideGroupSorters = ref<string[]>(["rating"])


</script>

<template>
  <v-container>
    <h1>Пивко</h1>

    <v-row class="pt-5" dense>
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
            v-model="selectedGroupSorters"
            chips
            label="Сортировка групп"
            :items="groupSorters"
            multiple
            variant="outlined"
            density="compact"
        ></v-select>
      </v-col>

      <v-col>
        <v-select
            v-model="selectedInsideGroupSorters"
            chips
            label="Сортировка внутри группы"
            :items="insideGroupSorters"
            multiple
            variant="outlined"
            density="compact"
        ></v-select>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col>
        <v-checkbox
            v-model="simplifyStyles"
            label="Упрощенные стили"
            density="compact"
        ></v-checkbox>
      </v-col>
    </v-row>

    <v-list>
      <template v-for="(groupContent, groupName) in groupedBeers" :key="groupName">
        <template v-if="groupName !== 'ungrouped'">
          <!-- Группа первого уровня -->
          <v-list-group>
            <template v-slot:activator="{ props }">
              <v-list-item
                  v-bind="props"
                  :title="`${groupName} (${isBeersArray(groupContent) ? 
                    groupContent.length : 
                    Object.values(groupContent).reduce((sum, arr) => sum + arr.length, 0)})`"
              />
            </template>

            <!-- Если это финальная группа с пивом -->
            <template v-if="isBeersArray(groupContent)">
              <v-list-item
                  v-for="beer in groupContent"
                  :key="`${beer.brewery}-${beer.name}`"
                  :href="beer.url"
                  :title="`${beer.brewery} — ${beer.name} (${beer.rating})`"
                  target="_blank"
                  density="compact"
              />
            </template>

            <!-- Если это подгруппа -->
            <template v-else>
              <v-list-group v-for="(subGroupBeers, subGroupName) in groupContent" :key="subGroupName">
                <template v-slot:activator="{ props }">
                  <v-list-item
                      v-bind="props"
                      :title="`${subGroupName} (${subGroupBeers.length})`"
                      density="compact"
                  />
                </template>

                <v-list-item
                    v-for="beer in subGroupBeers"
                    :key="`${beer.brewery}-${beer.name}`"
                    :href="beer.url"
                    :title="`${beer.brewery} — ${beer.name} (${beer.rating})`"
                    target="_blank"
                    density="compact"
                />
              </v-list-group>
            </template>
          </v-list-group>
        </template>

        <!-- Если нет группировки -->
        <template v-else>
          <v-list-item
              v-for="beer in groupContent"
              :key="`${beer.brewery}-${beer.name}`"
              :href="beer.url"
              :title="`${beer.brewery} — ${beer.name} (${beer.rating})`"
              target="_blank"
              density="compact"
          />
        </template>
      </template>
    </v-list>
  </v-container>
</template>

