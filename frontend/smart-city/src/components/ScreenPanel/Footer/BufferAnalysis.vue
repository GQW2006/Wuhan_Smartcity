<template>
  <div class="item">
    <!-- 底部按钮：点击展开/收起分析面板 -->
    <button
      class="toggle-btn"
      :class="{ active: showPanel }"
      @click="showPanel = !showPanel"
    >
      <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="9" />
        <circle cx="12" cy="12" r="4.5" />
        <circle cx="12" cy="12" r="1.2" fill="currentColor" />
      </svg>
    </button>
    <p>缓冲区分析</p>

    <!-- 分析面板：v-show 隐藏，隐藏时地图上的缓冲区图层保留 -->
    <div class="buffer-panel" v-show="showPanel">
      <div class="panel-head">
        <span class="panel-title">缓冲区分析</span>
        <button class="hide-btn" aria-label="隐藏面板" @click="showPanel = false">✕</button>
      </div>

      <div class="panel-body">
        <!-- 目标事故点选择 -->
        <el-select
          v-model="targetId"
          class="target-select"
          placeholder="选择目标事故点"
          filterable
          size="small"
        >
          <el-option
            v-for="e in eventOptions"
            :key="e.id"
            :label="`${e.event_num} · ${e.name}`"
            :value="e.id"
          />
        </el-select>

        <!-- 半径 + 分析 + 清除 -->
        <div class="form-row">
          <span class="form-label">半径(米)</span>
          <el-input-number
            v-model="distance"
            :min="100"
            :max="50000"
            :step="500"
            size="small"
          />
          <el-button
            type="primary"
            size="small"
            :loading="state.loading"
            :disabled="!targetId"
            @click="handleAnalyze"
          >
            分析
          </el-button>
          <el-button
            type="danger"
            size="small"
            plain
            :disabled="!state.analyzed"
            @click="handleClear"
          >
            清除
          </el-button>
        </div>

        <!-- 错误提示 -->
        <div v-if="state.error" class="error">{{ state.error }}</div>

        <!-- 分析结果 -->
        <template v-if="state.analyzed">
          <p class="summary">
            目标：{{ state.bufferInfo?.event_num || state.bufferInfo?.id }}（{{ state.bufferInfo?.name }}）
            <br />
            缓冲半径 {{ distance }}m，圈内其他事故点 {{ state.count }} 个
          </p>
          <el-table
            v-if="state.features.length"
            :data="state.features"
            size="small"
            :max-height="280"
            @row-click="rowClick"
          >
            <el-table-column prop="event_num" label="事件编号" />
            <el-table-column prop="name" label="类型" />
            <el-table-column prop="level" label="等级" width="60" />
          </el-table>
          <p v-else class="empty">该范围内没有其他事故点</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useSceneMap } from '@/composables/useSceneMap'
import { useEventBuffer } from '@/composables/useEventBuffer'
import { getEvents } from '@/api'

const sceneMap = useSceneMap()
const { state, analyzeBuffer, clearBufferResult } = useEventBuffer()

// 面板显隐（隐藏时地图上的缓冲图层保留，由 clearBufferResult 才真正清除）
const showPanel = ref(false)
// 目标事故点 id
const targetId = ref('')
// 缓冲区半径（米）
const distance = ref(1000)
// 事故点下拉选项（从 getEvents 取 Point 事件）
const eventOptions = ref([])

// 加载事故点列表，供下拉选择
onMounted(async () => {
  try {
    const res = await getEvents()
    eventOptions.value = (res.features || []).map((f) => ({
      id: f.properties.id,
      event_num: f.properties.event_num,
      name: f.properties.name,
      geometry: f.geometry,
    }))
  } catch (e) {
    state.error = e?.message || '事故点列表加载失败'
  }
})

// 执行分析：请求后端并渲染缓冲图层
async function handleAnalyze() {
  const { scene } = sceneMap.value
  if (!scene) return

  const target = eventOptions.value.find((e) => e.id === targetId.value)
  try {
    await analyzeBuffer(scene, targetId.value, distance.value)
    // 分析成功后飞行到目标事故点
    if (target?.geometry?.coordinates && sceneMap.value.map) {
      sceneMap.value.map.flyTo({
        center: target.geometry.coordinates,
        zoom: 14,
        pitch: 30,
        speed: 1,
      })
    }
  } catch (e) {
    // 错误信息已写入 state.error，由模板展示
  }
}

// 清除缓冲区：移除地图图层并清空结果数据（面板保留，可重新分析）
function handleClear() {
  clearBufferResult(sceneMap.value?.scene)
}

// 点击结果行：飞行到该事故点
function rowClick(row) {
  const { scene, map } = sceneMap.value
  if (!scene || !map || !row.geometry) return
  map.flyTo({
    center: row.geometry.coordinates,
    zoom: 15,
    speed: 1,
    pitch: 30,
  })
}

// 组件卸载时移除结果图层，避免残留
onBeforeUnmount(() => {
  clearBufferResult(sceneMap.value?.scene)
})
</script>

<style scoped>
/* 分析面板：固定在底部中央（参考 DisplayCard 的定位方式） */
.buffer-panel {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 90px;
  width: 380px;
  background: #536976d9;
  border-radius: 4px;
  box-shadow: 0 0 5px 3px rgba(0, 0, 0, 0.3);
  z-index: 10;
  color: #fff;
  text-align: left;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: rgba(0, 0, 0, 0.25);
  border-radius: 4px 4px 0 0;
}

.panel-title {
  font-size: 13px;
  font-weight: bold;
}

/* 隐藏按钮：隐藏面板（地图图层保留） */
.hide-btn {
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
}
.hide-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.panel-body {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.target-select {
  width: 100%;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-label {
  font-size: 12px;
  white-space: nowrap;
}

.error {
  color: #ff7875;
  font-size: 12px;
}

.summary {
  font-size: 12px;
  margin: 0;
  line-height: 1.6;
}

.empty {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  margin: 4px 0;
}

/* 暗色表格（与 DisplayCard 保持一致） */
:deep(.el-table) {
  background-color: transparent;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(0, 0, 0, 0.25);
  --el-table-header-text-color: #fff;
  --el-table-text-color: #fff;
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.08);
  --el-table-border-color: rgba(255, 255, 255, 0.15);
}
:deep(.el-table tr) {
  background-color: transparent;
  color: #fff;
  cursor: pointer;
}
:deep(.el-table th.el-table__cell),
:deep(.el-table td.el-table__cell) {
  background-color: transparent;
  border-bottom: none;
}
:deep(.el-table__inner-wrapper::before) {
  height: 0;
}
</style>
