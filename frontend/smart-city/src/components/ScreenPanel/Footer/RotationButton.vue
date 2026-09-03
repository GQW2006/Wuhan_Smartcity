<template>
  <div class="item">
    <button class="toggle-btn" @click="handleRotation">
      <img class="btn-icon" src="@/assets/icons/globe.svg" alt="自转" />
    </button>
    <p>{{ mark }}</p>
  </div>
</template>
<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useSceneMap } from '@/composables/useSceneMap'

// 自转开关: true 时地图持续自转, false 时停止(由按钮点击切换)
const moving = ref(true)
const sceneMap = useSceneMap()
let rafId = null // 当前动画帧 id, 用于卸载时取消循环

/* 每帧回调: requestAnimationFrame 按屏幕刷新率调用
 * 满足条件(地图就绪 / 开关开启 / 未放大到城市层级)时,
 * 把地图中心经度向右偏移一小段, 形成连续自转
 */
function rotateFrame() {
  const map = sceneMap.value?.map
  if (map && moving.value && map.getZoom() < 5) {
    const center = map.getCenter()
    center.lng += 0.1 // 每帧推进 0.1, 转速 = 0.1 × 刷新率
    // jumpTo 直接设置相机位置(无动画): 每帧微小跳变, 视觉上连续,
    map.jumpTo({ center })
  }
  // 无论是否推进, 都预约下一帧, 循环持续进行
  rafId = requestAnimationFrame(rotateFrame)
}

// 组件挂载后启动循环; 地图未就绪时每帧自动跳过, 就绪后即刻生效
onMounted(() => {
  rafId = requestAnimationFrame(rotateFrame)
})

/* 点击按钮: 切换自转开关 */
function handleRotation() {
  moving.value = !moving.value
}

// 按钮文案(随自转开关变化)
const mark = computed(() => {
  return moving.value ? '停止自转' : '开启自转'
})

// 卸载时取消循环, 防止回调操作已销毁的地图实例
onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
})
</script>
