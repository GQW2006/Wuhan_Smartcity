# 武汉智慧城市（Wuhan Smart City）

> 基于 **Vue 3 + Vite + Mapbox GL + AntV L7 / G2** 与 **Flask** 的武汉智慧城市三维可视化大屏。
> 通过 GeoJSON 数据接口，将武汉市建筑、道路、交通事件以 3D 地球/城市视角呈现，并配套图表统计面板与地图交互工具。

## ✨ 功能特性

- **3D 地球 / 城市双视角**
  - Mapbox 地球视角（globe 投影 + 大气层 `setFog`）与武汉城市视角自由切换
  - 地图自转开关（城市视角下自动停止自转）
- **城市三维场景**
  - 建筑楼层：`CityBuildingLayer`，按 `Elevation` 高度拉伸，含窗户亮色、扫光、悬停高亮动画
  - 道路网络：`LineLayer`，流线动画（trail）
- **大屏控制中心**
  - 出行人口统计（柱状图，动态增长）
  - 实时公交在线图（玫瑰图）
  - 人口统计图（饼图）
  - 武汉市三甲医院、高校学生统计（静态卡片）
- **地图交互工具**
  - 放大/缩小、鼠标位置、全屏、主题切换控件
  - 事故查询：框选矩形范围，结合 Turf.js 判断事故点是否在框内，结果表格展示并可定位
  - 测量工具：面积测量、距离测量、清除
- **大屏自适应**
  - 基于 1920×1080 设计稿的等比缩放（`ScreenScale`），任意窗口尺寸不挤压变形

## 🧱 技术栈

| 层 | 技术 |
| --- | --- |
| 前端框架 | Vue 3（Composition API + `<script setup>`） |
| 构建工具 | Vite |
| 地图/可视化 | Mapbox GL、AntV L7、AntV L7 Maps / Component / Draw |
| 图表 | AntV G2 v5 |
| 空间计算 | Turf.js（@turf/turf） |
| UI 组件 | Element Plus |
| HTTP | Axios |
| 后端 | Flask、Flask-CORS |
| 数据 | GeoJSON（FeatureCollection） |

## 📁 项目结构

```
Wuhan_Smartcity
├── backend                         # Flask 后端
│   ├── run.py                      # 启动入口（127.0.0.1:5000）
│   ├── config.py                   # 后端配置
│   ├── app
│   │   ├── __init__.py             # 应用工厂 & 蓝图注册
│   │   └── blueprints
│   │       ├── Wuhan_Buildings.py  # 建筑数据接口
│   │       ├── Wuhan_roads.py      # 道路数据接口
│   │       └── Wuhan_events.py     # 交通事件数据接口
│   ├── utils
│   │   └── respones.py             # 统一响应封装（ok / fail）
│   └── data
│       ├── Wuhan_Buildings.json    # 建筑轮廓（含 Elevation）
│       ├── Wuhan_roads.json        # 道路线数据（OSM）
│       └── Wuhan_events.json       # 交通事件点数据
└── frontend
    └── smart-city                  # Vue 3 前端
        ├── index.html
        ├── vite.config.js
        ├── .env                    # Mapbox Token 等环境变量
        ├── .env.development        # 开发环境 API 地址
        └── src
            ├── main.js             # 应用入口
            ├── App.vue             # 根组件
            ├── api                 # Axios 请求封装与接口定义
            ├── composables         # useSceneMap（provide/inject 共享地图场景）
            ├── assets              # 图标、图片、样式
            └── components
                ├── MapContainer.vue      # Mapbox + L7 Scene 初始化
                ├── MapControls.vue       # 地图控件
                ├── ScreenScale.vue       # 大屏等比缩放
                ├── SmartCity             # 建筑/道路图层加载
                └── ScreenPanel           # 图表面板、底部工具栏
```

## 🚀 快速开始

### 环境要求

- Node.js ≥ 18（建议 20+）
- Python ≥ 3.8

### 1. 启动后端

```bash
cd backend
pip install flask flask-cors

python run.py
# 默认运行在 http://127.0.0.1:5000
```

### 2. 启动前端

```bash
cd frontend/smart-city
npm install

npm run dev
```

打开终端输出的本地地址（默认 `http://localhost:5173`）即可访问。

> **注意**：前端依赖 Mapbox 底图，需保证 `frontend/smart-city/.env` 中的 `VITE_TOKEN` 有效。仓库内已内置一个示例 pk token，若失效请替换为自己的 Mapbox Access Token。

## 🔧 环境变量

前端环境变量位于 `frontend/smart-city/.env`：

| 变量 | 说明 |
| --- | --- |
| `VITE_TOKEN` | Mapbox 访问令牌（公开 pk token） |
| `VITE_API_BASE_URL` | 后端 API 地址，开发环境默认 `http://127.0.0.1:5000` |

> 如需发布到生产环境，建议在 Mapbox 后台为 token 配置 URL 白名单，避免 token 被盗用。

## 📡 接口说明

所有接口均返回统一结构：`{ "code": 0, "msg": "success", "data": ... }`。

### 建筑数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/Wuhan_Buildings/` | 获取全部建筑数据 |
| GET | `/Wuhan_Buildings/<id>` | 按 id 获取单个建筑 |
| POST | `/Wuhan_Buildings/` | 新增建筑（内存中追加） |
| DELETE | `/Wuhan_Buildings/<id>` | 按 id 删除建筑 |

### 道路数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/Wuhan_roads/` | 获取全部道路数据 |
| GET | `/Wuhan_roads/<id>` | 按 id 获取单条道路 |
| POST | `/Wuhan_roads/` | 新增道路 |
| DELETE | `/Wuhan_roads/<id>` | 按 id 删除道路 |

### 交通事件数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/Wuhan_events/` | 获取全部事件数据 |
| GET | `/Wuhan_events/<id>` | 按 id 获取单个事件 |
| POST | `/Wuhan_events/` | 新增事件 |
| DELETE | `/Wuhan_events/<id>` | 按 id 删除事件 |

> 说明：当前 `POST` / `DELETE` 仅修改后端内存中的数据，不会持久化回 JSON 文件；服务重启后恢复为原始数据。

## 🗂️ 数据说明

数据均以 GeoJSON `FeatureCollection` 格式存储于 `backend/data`：

- **Wuhan_Buildings.json**：建筑轮廓（`Polygon`），属性 `Elevation` 用于建筑高度拉伸。
- **Wuhan_roads.json**：道路线数据（`LineString`），属性含 `osm_id`、`name`、`type`。
- **Wuhan_events.json**：交通事件点数据（`Point`），属性含 `name`（类型）、`level`、`car_num`、`phone`、`event_num`、`area`。

## ⚠️ 注意事项

- 前端 `request.js` 使用 Axios 响应拦截器，约定后端 `code === 0` 表示成功，非 0 时 reject。
- `MapContainer.vue` 通过 `provide/inject`（`SCENE_MAP_KEY`）向子组件共享 L7 Scene 与 Mapbox Map 实例，需在 `MapContainer` 内部使用 `useSceneMap`。
- 后端 `__init__.py` 注册了 `Wuhan_Buildings`、`Wuhan_roads`、`Wuhan_events` 三个蓝图。
- 部分图表面板数据为前端本地模拟数据，如需接入真实数据，可在 `frontend/smart-city/src/components/ScreenPanel/Panels/` 下替换数据源。

## 📄 License

仅用于学习与演示。
