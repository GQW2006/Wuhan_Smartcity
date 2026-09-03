<template>
  <div class="item">
    <button class="toggle-btn" @click="toggleDraw">
      <img class="btn-icon" src="@/assets/icons/pen-tool.svg" alt="事故查询" />
    </button>
    <p>事故查询</p>
    <DisplayCard :tableData="dataSource" v-if="isShow" @close="handleClose" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useSceneMap } from '@/composables/useSceneMap'
import { DrawRect, DrawEvent } from '@antv/l7-draw'
import { point, polygon, booleanPointInPolygon } from '@turf/turf'
import DisplayCard from './DisplayCard.vue'

import { getEvents } from '@/api'

const sceneMap = useSceneMap()

let map = null
let scene = null
let draw = null
let eventsData = null
const dataSource = ref([])
const isShow = ref(false)

const toggleDraw = () => {
  // 1. 切换到城市视角
  map.flyTo({
    center: [114.3, 30.5],
    zoom: 12,
    pitch: 30,
  })
  // 2. 绘制矩形框
  if (draw) {
    draw.disable()
    draw.clear()
  }

  draw = new DrawRect(scene, {})
  draw.enable()
  draw.on(DrawEvent.Change, (allFeatures) => {
    // 保存最后绘制的图形
    const activeFeature = allFeatures[allFeatures.length - 1]
    // 只保留最后绘制的图形
    allFeatures.forEach((item, index) => {
      if (index !== allFeatures.length - 1) {
        draw.removeFeature(item)
      }
    })
    if (eventsData.length && activeFeature) {
      const {
        geometry: { coordinates: coordinatesActive },
      } = activeFeature

      // 使用turf判断哪些事故点落在绘制的拉框中
      const resData = eventsData.filter((item) => {
        const { geometry } = item
        if (geometry.type === 'Point') {
          // 基于坐标构建point和polygon
          const pt = point(geometry.coordinates)
          const poly = polygon(coordinatesActive)
          // 判断点是否在多边形内
          const isInArea = booleanPointInPolygon(pt, poly)
          return isInArea
        }
      })
      console.log(resData)
      dataSource.value = resData
      if (dataSource.value.length) {
        isShow.value = true
      }
    }
  })
}
const handleClose = () => {
  isShow.value = false
  if (draw) {
    draw.disable()
    draw.clear()
    draw = null
  }
  // 恢复城市视角
  map.flyTo({
    center: [114.3, 30.5],
    zoom: 12,
    pitch: 30,
  })
}
watch(
  sceneMap,
  (val) => {
    if (!val) return

    map = val.map
    scene = val.scene
  },
  {
    immediate: true,
  },
)
onMounted(async () => {
  const res = await getEvents()
  eventsData = res.features
})
</script>
