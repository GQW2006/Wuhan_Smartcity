<template></template>

<script setup>
import { watch, onBeforeUnmount } from "vue";
import { useSceneMap } from "@/composables/useSceneMap.js";
import useBuildings from "./hooks/useBuildings.js";
import useRoads from "./hooks/useRoads.js";
import { registerLayer, unregisterLayer } from "@/composables/useLayers.js";

const sceneMap = useSceneMap();
watch(sceneMap, async (Val) => {
  // 简洁版
  //   const building_layer = await useBuildings()
  //   sceneMap.value.scene.addLayer(building_layer)
  //   const roads_layer = await useRoads()
  //   sceneMap.value.scene.addLayer(roads_layer)
  if (!Val) return;

  const { scene } = Val;
  const [building_layer, roads_layer] = await Promise.all([
    useBuildings(),
    useRoads(),
  ]);
  scene.addLayer(building_layer);
  scene.addLayer(roads_layer);

  // ★ 新增：创建完图层后登记到面板（id 自定义，唯一即可）
  registerLayer({ id: "buildings", name: "武汉市建筑图", layer: building_layer });
  registerLayer({ id: "roads", name: "武汉市道路", layer: roads_layer });
});

// ★ 新增：组件卸载时注销，避免面板残留失效条目
onBeforeUnmount(() => {
  unregisterLayer("buildings");
  unregisterLayer("roads");
});
</script>

<style scoped></style>
