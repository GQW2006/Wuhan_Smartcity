<template>
  <div class="map-container">
    <!-- 地图容器: 由 Vue 管理 DOM 生命周期(模板 ref), 占满父容器 -->
    <div ref="mapEl" id="map" class="map-el"></div>
    <!-- 上层面板(子组件处于 MapContainer 内部, 可通过 inject 获取地图场景) -->
    <slot></slot>
  </div>
</template>

<script setup>
// 1. 初始化mapboxgl实例(map), 初始化L7的地图场景(scene)
// 2. 通过provide提供给后代组件使用
import { ref, shallowRef, onMounted, onBeforeUnmount, provide } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { Scene } from '@antv/l7'
import { Mapbox } from '@antv/l7-maps'

import { SCENE_MAP_KEY } from '@/composables/useSceneMap.js'

// 获取地图容器对应的dom元素
const mapEl = ref(null)

// 地图与场景实例对象层次比较深(shallowRef, 避免被 Vue 深度代理, 只保留第一层的代理)
const sceneMap = shallowRef(null)

onMounted(() => {
  // console.log(mapEl.value)
  // 1. 创建Mapbox的map实例对象
  const map = new mapboxgl.Map({
    container: mapEl.value, // 指定地图容器元素
    style: 'mapbox://styles/mapbox/dark-v11',
    center: [114.3, 30.5],
    zoom: 1,
    projection: 'globe',
    accessToken: import.meta.env.VITE_TOKEN,
  })
  map.on('style.load', () => {
    // 设置地球的大气层
    map.setFog({})
  })

  // 2. 创建L7的场景
  const scene = new Scene({
    id: 'map', // 指定地图容器的id, 给上面的div的id值保持一致
    map: new Mapbox({
      mapInstance: map,
    }), // 指定L7使用的底图, 将mapbox创建map对象和L7场景使用的底图关联
    // logoVisible: false, // 不显示L7的logo
  })
  // 设置sceneMap.value的值, 为后续组件提供地图场景和地图实例对象
  sceneMap.value = { scene, map }
})

onBeforeUnmount(() => {
  // 1. 销毁L7的场景
  sceneMap.value?.scene.destroy() // 确保不会出现undefined报错
  // 2. 销毁Mapbox的map实例
  sceneMap.value?.map.remove()
  sceneMap.value = null
})
// 3. 通过provide提供给后代组件使用
provide(SCENE_MAP_KEY, sceneMap)
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}
.map-el {
  width: 100%;
  height: 100%;
}
</style>

