<template>
  <div class="item">
    <el-popover
      placement="top"
      trigger="click"
      popper-style="background-color:#53697670;color:#fff"
      :width="120"
    >
      <template #reference>
        <button class="toggle-btn">
          <img class="btn-icon" src="@/assets/icons/ruler.svg" alt="测量" />
        </button>
      </template>
      <div class="popover-w column">
        <span
          v-for="item in tools"
          :key="item.tool"
          class="query-item"
          @click="handleClick(item.tool)"
        >
          {{ item.label }}
        </span>
      </div>
    </el-popover>
    <p>测量工具</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { DrawPolygon, DrawLine } from '@antv/l7-draw'

import { useSceneMap } from '@/composables/useSceneMap'

const sceneMap = useSceneMap()

let draw = null
let map = null
let scene = null

const tools = ref([
  {
    label: '测量面积',
    tool: 'DrawPolygon',
  },
  {
    label: '测量距离',
    tool: 'DrawLine',
  },
  {
    label: '清除',
    tool: 'Clear',
  },
])

const handleClick = (tool) => {
  // 1. 切换到城市视角
  map.flyTo({
    center: [114.3, 30.5],
    zoom: 12,
    pitch: 30,
  })

  if (draw) {
    draw.disable()
    draw.clear()
  }
  switch (tool) {
    case 'DrawPolygon':
      console.log('DrawPolygon')
      draw = new DrawPolygon(scene, {
        //展示面积
        areaOptions: {},
      })
      break
    case 'DrawLine':
      draw = new DrawLine(scene, {
        distanceOptions: {
          // 是否展示总距离
          showTotalDistance: false,
          // 是否展示一段的距离
          showDashDistance: true,
          // 展示的格式
          format: (meters) => {
            if (meters >= 1000) {
              return +(meters / 1000).toFixed(2) + 'km'
            } else {
              return +meters.toFixed(2) + 'm'
            }
          },
        },
      })
      break
    case 'Clear':
      if (draw) {
        draw.disable()
        draw.clear()
      }
      draw = null
      break
    default:
      return
  }
  if (draw) {
    draw.enable()
  }
}
watch(
  sceneMap,
  (val) => {
    if (!val) return
    map = val.map
    scene = val.scene
  },
  { immediate: true },
)
</script>

<style scoped>
/* 弹窗工具列表(el-popover 内容 teleport 到 body, 需在组件自身 scoped 内定义) */
.popover-w {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: stretch;
}
.query-item {
  padding: 4px 8px;
  color: #fff;
  cursor: pointer;
}
.query-item:hover {
  background: linear-gradient(
    to bottom,
    rgba(0, 128, 255, 0.6),
    rgba(0, 128, 255, 0.281)
  );
}
</style>
