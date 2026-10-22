/**
 * useEventBuffer - 事故点缓冲区分析（地图图层 + 结果数据）
 *
 * 职责划分：
 * - 本文件负责调用后端接口，并把返回的「缓冲区面 + 圈内事故点」渲染成 L7 图层
 * - BufferAnalysis.vue 只负责 UI（选点/输入距离/展示结果列表/面板显隐）
 *
 * 关键坑（同 useLayers.js）：L7 图层实例绝不放进 reactive/ref，
 * 否则 Vue 代理会破坏 L7 内部的 this 指向，导致切换/渲染异常。
 * 所以图层实例用普通模块变量保存，reactive 里只放可序列化的结果数据。
 */
import { reactive } from 'vue'
import { PolygonLayer, PointLayer } from '@antv/l7'
import { getEventBuffer } from '@/api'

// 结果图层实例（普通变量，不进 Vue 响应式系统）
let bufferLayer = null // 缓冲区面
let pointsLayer = null // 圈内事故点

// 可序列化结果（供组件模板渲染）
const state = reactive({
  loading: false,
  error: '',
  analyzed: false, // 是否已有分析结果
  count: 0, // 圈内其他事故点数量
  features: [], // 圈内事故点明细 [{ id, name, level, ... , geometry }]
  bufferInfo: null, // 缓冲区属性（目标点信息 + 半径）
})

/** 移除上一次的结果图层（分析新点位/清除时调用） */
function removeResultLayers(scene) {
  if (!scene) return
  if (bufferLayer) {
    scene.removeLayer(bufferLayer)
    bufferLayer = null
  }
  if (pointsLayer) {
    scene.removeLayer(pointsLayer)
    pointsLayer = null
  }
}

/**
 * 执行缓冲区分析：请求后端 -> 渲染缓冲区面 + 圈内事故点图层
 * @param {Object} scene L7 Scene 实例（useSceneMap 提供）
 * @param {String} eventId 目标事故点 id
 * @param {Number} distance 缓冲区半径（米），默认 1000
 * @returns 后端返回的 { buffer, events, count }
 */
export async function analyzeBuffer(scene, eventId, distance = 1000) {
  state.loading = true
  state.error = ''
  removeResultLayers(scene)
  try {
    const data = await getEventBuffer(eventId, distance)
    // 请求成功后重新移除旧层（失败时保留旧结果图层，便于用户重试）
    removeResultLayers(scene)

    // 1. 缓冲区面（半透明填充）
    bufferLayer = new PolygonLayer({ zIndex: 5 })
      .source({
        type: 'FeatureCollection',
        features: [data.buffer],
      })
      .shape('fill')
      .color('#ff5b5b')
      .style({ opacity: 0.3 })
    scene.addLayer(bufferLayer)

    // 2. 圈内事故点（高亮圆点，带白描边）
    pointsLayer = new PointLayer({ zIndex: 6 })
      .source(data.events)
      .shape('circle')
      .size(12)
      .color('#ffd200')
      .style({ opacity: 1, stroke: '#fff', strokeWidth: 2 })
    scene.addLayer(pointsLayer)

    // 3. 落结果数据（供模板渲染）
    state.count = data.count
    state.features = (data.events.features || []).map((f) => ({
      ...f.properties,
      geometry: f.geometry,
    }))
    state.bufferInfo = data.buffer?.properties || null
    state.analyzed = true
    return data
  } catch (e) {
    state.error = e?.message || '缓冲区分析失败'
    state.analyzed = false
    throw e
  } finally {
    state.loading = false
  }
}

/** 清除分析结果：移除图层并清空数据 */
export function clearBufferResult(scene) {
  removeResultLayers(scene)
  state.count = 0
  state.features = []
  state.bufferInfo = null
  state.error = ''
  state.analyzed = false
}

/** 组件统一入口 */
export function useEventBuffer() {
  return {
    state,
    analyzeBuffer,
    clearBufferResult,
  }
}
