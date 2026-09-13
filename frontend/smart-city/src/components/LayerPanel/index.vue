<template>
  <div class="layer-panel">
    <!-- 标题栏：点击可折叠 -->
    <div class="lp-header" @click="collapsed = !collapsed">
      <span class="lp-title">图层管理</span>
      <span class="lp-count">{{ visibleCount }} / {{ layers.length }}</span>
      <span class="lp-arrow" :class="{ collapsed }">▾</span>
    </div>

    <!-- 图层列表 -->
    <div v-show="!collapsed" class="lp-body">
      <p v-if="!layers.length" class="lp-empty">暂无已注册的图层</p>

      <div v-for="item in layers" :key="item.id" class="lp-item">
        <el-checkbox
          :model-value="item.visible"
          @change="(val) => toggleLayer(item.id, val)"
        />
        <span class="lp-name" :class="{ 'is-off': !item.visible }">{{ item.name }}</span>
      </div>

      <div class="lp-actions">
        <button class="lp-btn" @click="setAllVisible(true)">全部显示</button>
        <button class="lp-btn" @click="setAllVisible(false)">全部隐藏</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useLayers } from '@/composables/useLayers.js'

// 只取面板需要的能力：数据 + 两个动作
const { layers, toggleLayer, setAllVisible } = useLayers()

const collapsed = ref(false)
const visibleCount = computed(() => layers.filter((it) => it.visible).length)
</script>

<style scoped>
.layer-panel {
  position: absolute;
  /* 放在大屏左右两列(各 340px)之间的空隙里，避开面板区域；想换位置只改这四行 */
  top: 116px;
  left: 356px;
  width: 200px;
  z-index: 4; /* 要高于 ScreenPanel 的 z-index: 3 */
  pointer-events: auto; /* 面板需要接收点击 */
  background: rgba(8, 24, 44, 0.78);
  border: 1px solid rgba(25, 144, 255, 0.45);
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(25, 144, 255, 0.25);
  color: #cfe6ff;
  font-size: 13px;
  user-select: none;
}

/* 标题栏 */
.lp-header {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 10px;
  cursor: pointer;
  border-bottom: 1px solid rgba(25, 144, 255, 0.25);
  background: linear-gradient(90deg, rgba(25, 144, 255, 0.35), rgba(25, 144, 255, 0.05));
}
.lp-title { flex: 1; font-weight: 600; letter-spacing: 1px; }
.lp-count { color: #7fd4ff; font-size: 12px; }
.lp-arrow { transition: transform 0.2s; }
.lp-arrow.collapsed { transform: rotate(-90deg); }

/* 列表 */
.lp-body { padding: 8px 10px 10px; }
.lp-empty { margin: 6px 0; color: #6f8ba8; font-size: 12px; }
.lp-item { display: flex; align-items: center; gap: 6px; height: 28px; }
.lp-name { flex: 1; }
.lp-name.is-off { color: #6f8ba8; text-decoration: line-through; }

/* 操作按钮 */
.lp-actions { display: flex; gap: 8px; margin-top: 8px; }
.lp-btn {
  flex: 1;
  height: 26px;
  cursor: pointer;
  color: #cfe6ff;
  font-size: 12px;
  background: rgba(25, 144, 255, 0.15);
  border: 1px solid rgba(25, 144, 255, 0.45);
  border-radius: 4px;
}
.lp-btn:hover { background: rgba(25, 144, 255, 0.35); }

/* 调一下 Element Plus 复选框在深色背景下的观感 */
:deep(.el-checkbox__inner) {
  background-color: rgba(255, 255, 255, 0.06);
  border-color: rgba(25, 144, 255, 0.6);
}
:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #1990ff;
  border-color: #1990ff;
}
</style>