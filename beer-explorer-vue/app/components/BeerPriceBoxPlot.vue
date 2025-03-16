<script setup lang="ts">
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { compPricePerL } from "~/logic/beer";

// Регистрируем необходимые компоненты
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Props {
  historyData: any[];
}

const props = defineProps<Props>();

// Группируем данные по датам
const groupedByDate = computed(() => {
  const grouped = {};
  
  if (!props.historyData || props.historyData.length === 0) {
    return {};
  }
  
  props.historyData.forEach(item => {
    if (!item.date_parsed || !item.price || !item.volume) return;
    
    if (!grouped[item.date_parsed]) {
      grouped[item.date_parsed] = [];
    }
    
    // Используем цену за литр
    const pricePerLiter = compPricePerL(item.price, item.volume);
    grouped[item.date_parsed].push(pricePerLiter);
  });
  
  return grouped;
});

// Опции для графика
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Динамика цен за литр по дням'
    },
    tooltip: {
      callbacks: {
        title: (items) => {
          if (!items.length) return '';
          const item = items[0];
          return `Дата: ${item.label}`;
        },
        label: (item) => {
          const value = item.raw;
          return `${item.dataset.label}: ${value.toFixed(2)} ₽/л`;
        },
        footer: (items) => {
          if (!items.length) return '';
          const item = items[0];
          const date = item.label;
          const prices = groupedByDate.value[date];
          
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
      beginAtZero: true,
      title: {
        display: true,
        text: 'Цена за литр (₽/л)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Дата'
      }
    }
  }
};

// Подготавливаем данные для графика
const chartData = computed(() => {
  const labels = Object.keys(groupedByDate.value).sort();
  
  // Вычисляем минимальные, максимальные и средние значения для каждой даты
  const minValues = labels.map(date => {
    const prices = groupedByDate.value[date];
    return Math.min(...prices);
  });
  
  const maxValues = labels.map(date => {
    const prices = groupedByDate.value[date];
    return Math.max(...prices);
  });
  
  const avgValues = labels.map(date => {
    const prices = groupedByDate.value[date];
    return prices.reduce((a, b) => a + b, 0) / prices.length;
  });
  
  return {
    labels,
    datasets: [
      {
        label: 'Мин. цена за литр',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        data: minValues,
        fill: false,
        tension: 0.1
      },
      {
        label: 'Средняя цена за литр',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 2,
        data: avgValues,
        fill: false,
        tension: 0.1
      },
      {
        label: 'Макс. цена за литр',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        data: maxValues,
        fill: false,
        tension: 0.1
      }
    ]
  };
});
</script>

<template>
  <div v-if="Object.keys(groupedByDate).length > 0" class="chart-container" style="position: relative; height: 300px;">
    <Line 
      :data="chartData" 
      :options="chartOptions"
    />
  </div>
  <div v-else class="text-center pa-4">
    Недостаточно данных для построения графика
  </div>
</template> 