<template></template>

<script setup>
import { watch } from "vue";
import { useSceneMap } from "@/composables/useSceneMap.js";
import useBuildings from "./hooks/useBuildings.js";
import useRoads from "./hooks/useRoads.js";

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
});
</script>

<style scoped></style>
