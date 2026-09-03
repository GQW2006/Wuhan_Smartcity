// 导入数据接口
import { getRoads } from '@/api'

// 导入线图层
import { LineLayer } from '@antv/l7'

// 导出hooks函数, 创建城市道路图层
export default async () => {
  // 1. 获取数据
  const roads_data = await getRoads()

  // 2. 创建线图层
  const roads_layer = new LineLayer({
    name: '武汉市道路',
  })
    .source(roads_data)
    .size(1)
    .shape('line')
    .color('#1990FF')
    .animate({
      trailLength: 2, // 流线长度
      duration: 2, // 持续时间
      interval: 1, // 间隔周期
    })
    .filter('coordinates', (evt) => evt.length > 20)

  // 3. 返回线图层
  return roads_layer
}
