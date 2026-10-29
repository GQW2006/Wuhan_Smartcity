<template>
  <div class="item">
    <button
      class="toggle-btn"
      :class="{ active: isDrawing }"
      @click="toggleDraw"
    >
      <img class="btn-icon" src="@/assets/icons/pen-tool.svg" alt="事故查询" />
    </button>
    <p>事故查询</p>
    <DisplayCard :tableData="dataSource" v-if="isShow" @close="handleClose" />
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import { useSceneMap } from '@/composables/useSceneMap'
import { useBoxQuery } from '@/composables/useBoxQuery'
import DisplayCard from './DisplayCard.vue'

const sceneMap = useSceneMap()
const { startBoxQuery, stopBoxQuery } = useBoxQuery()

let map = null
let scene = null
const dataSource = ref([]) // 后端返回的要素
const isShow = ref(false) // 结果表格显隐
const isDrawing = ref(false) // 是否处于框选状态

watch(
  sceneMap,
  (val) => {
    if (!val) return
    map = val.map
    scene = val.scene
  },
  { immediate: true },
)

// 切换框选：再次点击则结束并清除
const toggleDraw = () => {
  if (!map || !scene) return

  if (isDrawing.value) {
    handleClose()
    return
  }

  // 1. 切回城市视角
  map.flyTo({ center: [114.3, 30.5], zoom: 12, pitch: 30 })
  // 2. 清空上一次结果
  dataSource.value = []
  isShow.value = false
  isDrawing.value = true

  // 3. 开始框选：绘制完成后由 useBoxQuery 调用后端并高亮结果
  startBoxQuery(scene, {
    layer: 'events',
    onResult: (features) => {
      dataSource.value = features
      if (features.length) isShow.value = true
    },
  })
}

const handleClose = () => {
  isShow.value = false
  dataSource.value = []
  isDrawing.value = false
  stopBoxQuery(scene)
  // 恢复城市视角
  map?.flyTo({ center: [114.3, 30.5], zoom: 12, pitch: 30 })
}

onBeforeUnmount(() => stopBoxQuery(scene))
</script>
