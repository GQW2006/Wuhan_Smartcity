<template></template>

<script setup>
import { useSceneMap } from "@/composables/useSceneMap.js";
import { Logo, Zoom, MouseLocation, Fullscreen, MapTheme } from "@antv/l7-component";
// import logo from "@/assets/img/image.png";
import { watch } from "vue";



const sceneMap = useSceneMap();

watch(sceneMap, (Val) => {
  if (!Val) return;

  const { scene } = Val;

    // 添加logo控件
//   const logoControl = new Logo({
//     img: logo,
//     url: "https://www.baidu.com",
//   });
//   scene.addControl(logoControl);

  // 鼠标位置控件
  const mouseLocation = new MouseLocation({
    transform: ([lng, lat]) => [+lng.toFixed(4), +lat.toFixed(4)],
    position: "bottomright",
  });
  scene.addControl(mouseLocation);

  // 添加放大缩小控件
  const zoom = new Zoom({
    zoomInTitle: "放大",
    zoomOutTitle: "缩小",
    position: "bottomright",
  });
  scene.addControl(zoom);

  // 添加全屏控件
  const fullscreen = new Fullscreen({
    btnText: '全屏',
    exitBtnText: '退出全屏',
  })
  scene.addControl(fullscreen)

  // 主题切换控件
  const mapTheme = new MapTheme()
  scene.addControl(mapTheme)
});
</script>

<style scoped></style>
