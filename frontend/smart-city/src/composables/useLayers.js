import { reactive, readonly } from 'vue'

/**
 * 图层注册表（模块级单例）
 *
 * 为什么需要它：创建图层的组件（SmartCity）和操作图层的组件（LayerPanel）互不认识，
 * 中间靠这张注册表通信 —— 谁建的图层谁登记，面板只负责显示与切换显隐。
 *
 * ⚠️ 关键坑：L7 的图层实例绝对不要放进 reactive / ref 里！
 * Vue 的 reactive 会递归代理对象，而 L7 内部大量依赖 this 指向与实例比较，
 * 被代理后容易出现"切换没反应 / 渲染错乱"这类极难排查的问题。
 * 所以：可序列化的信息（id/name/visible）放 reactive，L7 实例放普通 Map。
 */

// 面板要用的数据（纯数据，安全地被 Vue 代理）
const state = reactive({
  layers: [], // [{ id, name, visible }]
})

// L7 图层实例：id -> layer（普通 Map，刻意不进 Vue 的响应式系统）
const instances = new Map()

const layersRO = readonly(state.layers)

// 本地图层清单（后端 /api/layers 还没接，先把"要管哪些图层"写在这里当配置）
export const LOCAL_LAYERS = [
  { id: 'buildings', name: '武汉市建筑图', visible: true },
  { id: 'roads', name: '武汉市道路', visible: true },
  { id: 'events', name: '武汉交通事件', visible: false },
]

/** L7 2.x 的 BaseLayer 提供 show()/hide()/isVisible()，这里做一层容错封装 */
function applyVisible(layer, visible) {
  if (!layer) return
  if (visible) layer.show?.()
  else layer.hide?.()
}

/** 注册一个图层（同一个 id 重复注册视为更新，避免热更新/重复挂载出现两条） */
export function registerLayer({ id, name, layer, visible = true }) {
  if (!id) throw new Error('registerLayer 需要一个唯一的 id')

  instances.set(id, layer)

  const item = { id, name: name || id, visible }
  const idx = state.layers.findIndex((it) => it.id === id)
  if (idx > -1) state.layers[idx] = item
  else state.layers.push(item)

  // 注册时就与图层的真实状态对齐
  applyVisible(layer, visible)
  return item
}

/** 注销图层（组件卸载时调用，避免面板里留着一个已经销毁的图层） */
export function unregisterLayer(id) {
  instances.delete(id)
  const idx = state.layers.findIndex((it) => it.id === id)
  if (idx > -1) state.layers.splice(idx, 1)
}

/** 切换单个图层的显隐：visible 传布尔值=强制设置，不传=取反 */
export function toggleLayer(id, visible) {
  const item = state.layers.find((it) => it.id === id)
  if (!item) return
  item.visible = typeof visible === 'boolean' ? visible : !item.visible
  applyVisible(instances.get(id), item.visible)
}

/** 全部显示 / 全部隐藏 */
export function setAllVisible(visible) {
  state.layers.forEach((it) => {
    it.visible = visible
    applyVisible(instances.get(it.id), visible)
  })
}

/** 组件里的统一入口，用法和 useSceneMap 保持一致 */
export function useLayers() {
  return {
    layers: layersRO,
    registerLayer,
    unregisterLayer,
    toggleLayer,
    setAllVisible,
  }
}