// 导入接口函数
// @表示src的路径, api后面什么都不写就表示加载默认的index.js
import { getCityBuildings } from '@/api'

import { CityBuildingLayer } from '@antv/l7'

// 默认导出函数
export default async () => {
  // 获取城市建筑数据
  const buildings_data = await getCityBuildings()

  console.log("=================后端返回数据=================", buildings_data.features)

  // 创建城市建筑图层
  const building_layer = new CityBuildingLayer({
    name: '武汉市建筑图',
  })

  // 设置图层的属性
  building_layer
    .source(buildings_data) // 设置数据源
    .size('Elevation', (h) => h) // 根据'Elevation字段'设置大小
    .animate(true) // 开启动画
    .active({
      color: '#0ff', // 鼠标悬停时颜色
      mix: 0.5, // 混合比例
    }) // 鼠标悬停时效果
    .style({
      opacity: 0.7,
      baseColor: 'rgb(16, 16, 16)', // 建筑的基础底色
      windowColor: 'rgb(30, 60, 89)', // 窗户颜色
      brightColor: 'rgb(255, 176, 38)', // 亮色
      sweep: {
        enable: true,
        sweepRadius: 2,
        sweepColor: '#1990FF',
        sweepSpeed: 0.3,
        sweepCenter: [114.3, 30.5],
      }, // 开启扫过效果
    }) // 设置楼房样式

  return building_layer
}


  

