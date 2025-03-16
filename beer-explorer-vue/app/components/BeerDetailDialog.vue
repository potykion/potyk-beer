<script lang="ts" setup>
import type { Beer } from "~/logic/beer";

interface Props {
  beer: Beer;
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:isOpen']);

const beerHistory = ref([]);
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
    
    beerHistory.value = data.value || [];
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
</script>

<template>
  <v-dialog :model-value="isOpen" @update:model-value="closeDialog" max-width="800px">
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
          </v-col>
        </v-row>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="text-h6 mb-3">История цен</div>
        
        <v-progress-circular
          v-if="isLoading"
          indeterminate
          color="primary"
          class="ma-4"
        ></v-progress-circular>
        
        <v-data-table
          v-else-if="beerHistory && beerHistory.length > 0"
          :headers="[
            { title: 'Дата', key: 'date_parsed' },
            { title: 'Магазин', key: 'venue' },
            { title: 'Объем', key: 'volume' },
            { title: 'Цена', key: 'price' }
          ]"
          :items="beerHistory"
          class="elevation-1"
        ></v-data-table>
        <div v-else class="text-center pa-4">
          Нет данных по истории цен
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template> 