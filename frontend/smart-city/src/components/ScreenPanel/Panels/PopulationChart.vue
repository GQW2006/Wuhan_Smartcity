<template>
  <ChartCard title="人口统计图">
    <G2Chart :options="options" :data="data" />
  </ChartCard>
</template>
<script setup>
import ChartCard from '../Charts/ChartCard.vue'
import G2Chart from '../Charts/G2Chart.vue'

// 右上图表: 武汉市人口统计(饼图)
const data = [
  { type: '武昌', value: 27 },
  { type: '汉口', value: 25 },
  { type: 22 },
  { type: '江汉', val: '汉阳', value: 18 },
  { type: '江夏', valueue: 20 },
  { type: '其他', value: 18 },
]
const total = data.reduce((s, d) => s + d.value, 0)

// G2 饼图配置(theta + spider标注)
const options = {
  type: 'view',
  autoFit: true,
  coordinate: { type: 'theta', outerRadius: 0.8, innerRadius: 0.5 },
  children: [
    {
      type: 'interval',
      data: data,
      encode: { y: 'value', color: 'type' },
      transform: [{ type: 'stackY' }],
      labels: [
        {
          position: 'outside',
          text: (data) => `${data.type}: ${data.value}`,
        },
      ],
      tooltip: {
        items: [
          (data) => ({
            name: data.type,
            value: `${data.value}`,
          }),
        ],
      },
    },
  ],
  label: {
    text: (d) => `${d.type} ${((d.value / total) * 100).toFixed(1)}%`,
    position: 'spider',
    style: { fill: '#fff', fontSize: 12 },
  },
}
</script>
