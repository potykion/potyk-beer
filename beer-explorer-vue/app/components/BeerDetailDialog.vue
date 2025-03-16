<script lang="ts" setup>
import type { Beer } from "~/logic/beer";
import { compPricePerL } from "~/logic/beer";
import BeerPriceBoxPlot from "~/components/BeerPriceBoxPlot.vue";
import BeerPriceByVenueChart from "~/components/BeerPriceByVenueChart.vue";

interface Props {
  beer: Beer;
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:isOpen']);

const beerHistory = ref<any[]>([]);
const isLoading = ref(false);

// Следим за изменением состояния диалогового окна
watch(() => props.isOpen, async (newValue) => {
  if (newValue && props.beer?.url) {
    await fetchBeerHistory();
  }
});

// Функция для получения истории цен пива
const fetchBeerHistory = async () => {
  if (!props.beer?.url) return;
  
  isLoading.value = true;
  try {
    const { data } = await useFetch('/api/beer-history', {
      method: 'POST',
      body: {
        url: props.beer.url
      }
    });
    
    beerHistory.value = Array.isArray(data.value) ? data.value : [];
  } catch (error) {
    console.error('Ошибка при получении истории цен:', error);
  } finally {
    isLoading.value = false;
  }
};

// При монтировании компонента, если диалог открыт, получаем историю
onMounted(async () => {
  if (props.isOpen && props.beer?.url) {
    await fetchBeerHistory();
  }
});

const closeDialog = () => {
  emit('update:isOpen', false);
};

// Активная вкладка
const activeTab = ref(0);

// Вычисляем цену за литр для отображения в таблице
const tableItems = computed(() => {
  if (!beerHistory.value || beerHistory.value.length === 0) {
    return [];
  }
  
  return beerHistory.value.map(item => {
    const pricePerLiter = item.volume ? compPricePerL(item.price, item.volume) : null;
    
    return {
      ...item,
      price_per_liter: pricePerLiter !== null ? pricePerLiter.toFixed(2) : 'Н/Д'
    };
  });
});
</script>

<template>
  <v-dialog :model-value="isOpen" @update:model-value="closeDialog" max-width="900px">
    <v-card>
      <v-card-title class="d-flex align-center">
        <span class="text-h5">{{ beer.name }}</span>
        <v-spacer></v-spacer>
        <v-btn icon @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="4">
            <v-img
              v-if="beer.img"
              :src="beer.img"
              :lazy-src="beer.img"
              max-height="200"
              contain
              class="mx-auto"
            />
          </v-col>
          
          <v-col cols="12" sm="8">
            <div class="text-h6 mb-2">{{ beer.brewery }}</div>
            <div class="text-subtitle-1 mb-2">{{ beer.style }}</div>
            <div class="d-flex align-center mb-2">
              <span class="font-weight-bold mr-2">ABV:</span> {{ beer.abv }}%
            </div>
            <div class="d-flex align-center mb-2">
              <span class="font-weight-bold mr-2">IBU:</span> {{ beer.ibu }}
            </div>
            <div class="d-flex align-center mb-2">
              <span class="font-weight-bold mr-2">Рейтинг:</span> {{ beer.rate }}
            </div>
            <div class="d-flex align-center mb-2">
              <v-btn 
                v-if="beer.url" 
                :href="beer.url" 
                target="_blank" 
                prepend-icon="mdi-open-in-new"
                variant="outlined"
                size="small"
                class="mt-2"
              >
                Открыть на Untappd
              </v-btn>
            </div>
          </v-col>
        </v-row>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="text-h6 mb-3">История цен</div>
        
        <v-progress-circular
          v-if="isLoading"
          indeterminate
          color="primary"
          class="ma-4 d-block mx-auto"
        ></v-progress-circular>
        
        <template v-else>
          <v-tabs v-model="activeTab" bg-color="primary">
            <v-tab value="0">График по дням</v-tab>
            <v-tab value="1">График по магазинам</v-tab>
            <v-tab value="2">Таблица</v-tab>
          </v-tabs>
          
          <v-window v-model="activeTab">
            <v-window-item value="0">
              <div class="pa-4">
                <BeerPriceBoxPlot :history-data="beerHistory" />
              </div>
            </v-window-item>
            
            <v-window-item value="1">
              <div class="pa-4">
                <BeerPriceByVenueChart :history-data="beerHistory" />
              </div>
            </v-window-item>
            
            <v-window-item value="2">
              <v-data-table
                v-if="beerHistory && beerHistory.length > 0"
                :headers="[
                  { title: 'Дата', key: 'date_parsed' },
                  { title: 'Магазин', key: 'venue' },
                  { title: 'Объем', key: 'volume' },
                  { title: 'Цена', key: 'price', align: 'end' },
                  { title: 'Цена за литр', key: 'price_per_liter', align: 'end' }
                ]"
                :items="tableItems"
                class="elevation-1"
                :items-per-page="10"
                :footer-props="{
                  'items-per-page-options': [10, 20, 50, -1],
                  'items-per-page-text': 'Строк на странице'
                }"
              >
                <template v-slot:item.price="{ item }">
                  {{ item.price }} ₽
                </template>
                <template v-slot:item.price_per_liter="{ item }">
                  {{ item.price_per_liter }} ₽/л
                </template>
              </v-data-table>
              <div v-else class="text-center pa-4">
                Нет данных по истории цен
              </div>
            </v-window-item>
          </v-window>
        </template>
      </v-card-text>
    </v-card>
  </v-dialog>
</template> 