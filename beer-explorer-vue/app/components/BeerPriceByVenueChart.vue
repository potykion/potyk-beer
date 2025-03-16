<script setup lang="ts">
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { compPricePerL } from "~/logic/beer";

// Регистрируем необходимые компоненты
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Props {
  historyData: any[];
}

const props = defineProps<Props>();

// Группируем данные по магазинам
const groupedByVenue = computed(() => {
  const grouped = {};
  
  if (!props.historyData || props.historyData.length === 0) {
    return {};
  }
  
  props.historyData.forEach(item => {
    if (!item.venue || !item.price || !item.volume) return;
    
    if (!grouped[item.venue]) {
      grouped[item.venue] = [];
    }
    
    // Используем цену за литр
    const pricePerLiter = compPricePerL(item.price, item.volume);
    grouped[item.venue].push(pricePerLiter);
  });
  
  return grouped;
});

// Опции для графика
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y', // Горизонтальный бар-график
  plugins: {
    title: {
      display: true,
      text: 'Цены за литр по магазинам'
    },
    tooltip: {
      callbacks: {
        title: (items) => {
          if (!items.length) return '';
          const item = items[0];
          return `Магазин: ${item.label}`;
        },
        label: (item) => {
          const value = item.raw;
          return `${item.dataset.label}: ${value.toFixed(2)} ₽/л`;
        },
        footer: (items) => {
          if (!items.length) return '';
          const item = items[0];
          const venue = item.label;
          const prices = groupedByVenue.value[venue];
          
          if (!prices || !prices.length) return '';
          
          const min = Math.min(...prices);
          const max = Math.max(...prices);
          const avg = prices.reduce((a, b) => a + b, 0) / prices.length;
          
          return [
            `Мин: ${min.toFixed(2)} ₽/л`,
            `Макс: ${max.toFixed(2)} ₽/л`,
            `Средняя: ${avg.toFixed(2)} ₽/л`,
            `Кол-во цен: ${prices.length}`
          ];
        }
      }
    }
  },
  scales: {
    y: {
      title: {
        display: true,
        text: 'Магазин'
      }
    },
    x: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Цена за литр (₽/л)'
      }
    }
  }
};

// Подготавливаем данные для графика
const chartData = computed(() => {
  const labels = Object.keys(groupedByVenue.value).sort();
  
  // Вычисляем минимальные, максимальные и средние значения для каждого магазина
  const minValues = labels.map(venue => {
    const prices = groupedByVenue.value[venue];
    return Math.min(...prices);
  });
  
  const maxValues = labels.map(venue => {
    const prices = groupedByVenue.value[venue];
    return Math.max(...prices);
  });
  
  const avgValues = labels.map(venue => {
    const prices = groupedByVenue.value[venue];
    return prices.reduce((a, b) => a + b, 0) / prices.length;
  });
  
  return {
    labels,
    datasets: [
      {
        label: 'Мин. цена за литр',
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        data: minValues
      },
      {
        label: 'Средняя цена за литр',
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 1,
        data: avgValues
      },
      {
        label: 'Макс. цена за литр',
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        data: maxValues
      }
    ]
  };
});
</script>

<template>
  <div v-if="Object.keys(groupedByVenue).length > 0" class="chart-container" style="position: relative; height: 300px;">
    <Bar 
      :data="chartData" 
      :options="chartOptions"
    />
  </div>
  <div v-else class="text-center pa-4">
    Недостаточно данных для построения графика
  </div>
</template> 