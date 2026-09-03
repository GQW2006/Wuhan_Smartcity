<template>
  <div class="item">
    <button class="toggle-btn" @click="flyTo">
      <img class="btn-icon" src="@/assets/icons/crosshair.svg" alt="切换" />
    </button>
    <p>{{ flyMsg }}</p>
  </div>
</template>
<script setup>
import { computed, ref } from 'vue'
import { useSceneMap } from '@/composables/useSceneMap'

const sceneMap = useSceneMap()
const isCityView = ref(false)

// 按钮文案: 当前视角 -> 点击后要切换到的目标视角
const flyMsg = computed(() => {
  return isCityView.value ? '地球视角' : '城市视角'
})

// 城市/地球视角切换飞行
function flyTo() {
  const { map, scene } = sceneMap.value || {}
  if (!map || !scene) return

  isCityView.value = !isCityView.value

  if (isCityView.value) {
    map.flyTo({
      center: [114.3, 30.5],
      zoom: 14,
      pitch: 70,
    })
  } else {
    map.flyTo({
      center: [114.3, 30.5],
      zoom: 1,
      pitch: 0,
    })
  }
}
</script>
