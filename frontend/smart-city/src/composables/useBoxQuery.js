/**
 * useBoxQuery - 框选查询（画框 → 调后端 bbox 接口 → 高亮结果）
 *
 * 职责划分：
 * - 本文件负责绘制矩形、把矩形转成 bbox、请求后端并渲染高亮图层
 * - EventsQuery.vue 只负责按钮与结果表格展示
 *
 * 关键坑（同 useLayers.js）：L7 图层实例绝不放进 reactive/ref，
 * 否则 Vue 代理会破坏 L7 内部的 this 指向；所以实例用普通变量保存。
 */
import { reactive } from 'vue'
import { PointLayer, LineLayer, PolygonLayer } from '@antv/l7'
import { DrawRect, DrawEvent } from '@antv/l7-draw'
import { getSpatialByBbox } from '@/api'

const state = reactive({
  loading: false,
  error: '',
  features: [], // 后端返回的要素（GeoJSON Feature）
})

let draw = null // 绘制矩形实例
let resultLayer = null // 查询结果高亮图层
let timer = null // 拖动过程防抖

/** 从 DrawRect 的多边形坐标中提取 bbox：[minx, miny, maxx, maxy] */
function toBbox(coordinates) {
  const ring = coordinates[0]
  const xs = ring.map((c) => c[0])
  const ys = ring.map((c) => c[1])
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]
}

/** 按要素类型选择高亮图层：点→圆点，线→线，面→半透明填充 */
function createHighlightLayer(features) {
  const data = { type: 'FeatureCollection', features }
  const type = features[0]?.geometry?.type || ''

  if (type === 'Point' || type === 'MultiPoint') {
    return new PointLayer({ zIndex: 8 })
      .source(data)
      .shape('circle')
      .size(14)
      .color('#ffd200')
      .style({ opacity: 1, stroke: '#fff', strokeWidth: 2 })
  }
  if (type === 'LineString' || type === 'MultiLineString') {
    return new LineLayer({ zIndex: 8 })
      .source(data)
      .shape('line')
      .size(2)
      .color('#00e5ff')
  }
  return new PolygonLayer({ zIndex: 8 })
    .source(data)
    .shape('fill')
    .color('#00e5ff')
    .style({ opacity: 0.35 })
}

/** 请求后端并渲染高亮结果 */
async function runQuery(scene, layer, bbox, onResult) {
  state.loading = true
  state.error = ''
  try {
    const fc = await getSpatialByBbox({ layer, bbox })
    state.features = fc.features || []

    // 移除上一次的高亮图层后再渲染
    if (resultLayer) {
      scene.removeLayer(resultLayer)
      resultLayer = null
    }
    if (state.features.length) {
      resultLayer = createHighlightLayer(state.features)
      scene.addLayer(resultLayer)
    }

    onResult?.(state.features)
  } catch (e) {
    state.features = []
    state.error = e?.message || '框选查询失败'
    onResult?.([])
  } finally {
    state.loading = false
  }
}

/**
 * 开始框选：启用矩形绘制，绘制完成后自动请求后端并高亮
 * @param {Object} scene L7 Scene 实例
 * @param {Object} options { layer: 'events'|'roads'|'buildings', onResult(features) }
 */
export function startBoxQuery(scene, { layer = 'events', onResult } = {}) {
  stopBoxQuery(scene)

  draw = new DrawRect(scene, {})
  draw.enable()
  draw.on(DrawEvent.Change, (allFeatures) => {
    // 已停止框选时忽略残留事件
    if (!draw) return

    // 只保留最后绘制的矩形
    const active = allFeatures[allFeatures.length - 1]
    allFeatures.forEach((f, i) => {
      if (i !== allFeatures.length - 1) draw?.removeFeature(f)
    })
    if (!active) return

    const bbox = toBbox(active.geometry.coordinates)
    // 拖动过程中会连续触发，防抖后再请求
    clearTimeout(timer)
    timer = setTimeout(() => runQuery(scene, layer, bbox, onResult), 300)
  })
}

/** 停止框选并清除高亮图层与结果数据 */
export function stopBoxQuery(scene) {
  clearTimeout(timer)

  if (draw) {
    draw.disable()
    draw.clear()
    draw = null
  }
  if (resultLayer && scene) {
    scene.removeLayer(resultLayer)
    resultLayer = null
  }

  state.loading = false
  state.error = ''
  state.features = []
}

/** 组件统一入口 */
export function useBoxQuery() {
  return { state, startBoxQuery, stopBoxQuery }
}
