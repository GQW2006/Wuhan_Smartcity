# 武汉智慧城市（Wuhan Smart City）

> 基于 **Vue 3 + Vite + Mapbox GL + AntV L7 / G2** 前端与 **Flask + PostgreSQL / PostGIS** 后端的武汉智慧城市三维可视化大屏。
> 前端通过 GeoJSON 接口渲染武汉建筑、道路、交通事件，配套图表统计面板与地图交互工具；
> 后端基于 PostGIS 提供空间查询能力（如事故点缓冲区分析）。

## ✨ 功能特性

- **3D 地球 / 城市双视角**
  - Mapbox 地球视角（globe 投影 + 大气层 `setFog`）与武汉城市视角自由切换
  - 地图自转开关（城市视角下自动停止自转）
- **城市三维场景**
  - 建筑楼层：`CityBuildingLayer`，按 `Elevation` 高度拉伸，含窗户亮色、扫光、悬停高亮动画
  - 道路网络：`LineLayer`，流线动画（trail）
- **大屏控制中心**
  - 出行人口统计（柱状图）、实时公交在线（玫瑰图）、人口统计（饼图）、三甲医院 / 高校统计卡片
  - 控制中心按钮可整体隐藏 / 展开左右图表列
- **事故查询（框选 + 后端空间查询）**
  - 地图上拖拽绘制矩形，前端将矩形转为 bbox 调用后端 `GET /api/spatial/bbox`
  - 后端 PostGIS `ST_MakeEnvelope` + `ST_Intersects` 完成范围过滤，返回 GeoJSON
  - 结果在地图上高亮（点→黄色圆点 / 线→青色线 / 面→半透明填充），并以表格展示，点击行定位到该事故点
- **缓冲区分析（PostGIS）**
  - 后端 `ST_Buffer` 对目标事故点生成指定半径（米）缓冲区，`ST_DWithin` 判断圈内是否存在其他事故点
  - 前端 L7 `PolygonLayer` / `PointLayer` 渲染缓冲面与圈内高亮点
  - 面板支持隐藏 / 展开与一键清除（隐藏时地图图层保留）
- **图层管理**
  - `useLayers` 注册 / 注销 / 显隐统一管理（建筑、道路、事件图层）
- **测量工具与地图控件**
  - 面积测量、距离测量、清除；放大缩小、鼠标位置、全屏、主题切换
- **大屏自适应**
  - 基于 1920×1080 设计稿等比缩放（`ScreenScale`），任意窗口尺寸不挤压变形

## 🧱 技术栈

| 层 | 技术 |
| --- | --- |
| 前端框架 | Vue 3（Composition API + `<script setup>`） |
| 构建工具 | Vite（`/api` 代理到后端，解决跨域） |
| 地图 / 可视化 | Mapbox GL、AntV L7、AntV L7 Maps / Component / Draw |
| 图表 | AntV G2 v5 |
| 空间计算（前端） | Turf.js（@turf/turf） |
| 空间查询（后端） | PostGIS（ST_MakeEnvelope / ST_Intersects / ST_Buffer / ST_DWithin） |
| UI 组件 | Element Plus |
| HTTP | Axios |
| 后端框架 | Flask、flask-smorest、Flask-JWT-Extended |
| ORM / 空间数据 | SQLAlchemy、geoalchemy2、psycopg2 |
| 数据库 | PostgreSQL + PostGIS（空间扩展） |

## 📁 项目结构

```
Wuhan_Smartcity
├── .gitignore                 # 忽略 venv / __pycache__ / .env 等
├── README.md
├── backend                    # Flask 后端
│   ├── run.py                 # 启动入口（127.0.0.1:5000）
│   ├── run.bat                # Windows 一键启动（自动使用 venv）
│   ├── config.py              # 配置（DATABASE_URL 等，读取 .env）
│   ├── extensions.py          # db / migrate / api / jwt 扩展实例
│   ├── schemas.py             # flask-smorest 输入 / 输出序列化 Schema
│   ├── services
│   │   ├── event_buffer.py    # 缓冲区分析服务（ST_Buffer / ST_DWithin）
│   │   └── spatial_query.py   # bbox 空间查询服务（ST_MakeEnvelope / ST_Intersects）
│   ├── utils
│   │   └── respones.py        # 统一响应封装（ok / fail / ok_geojson）
│   ├── app
│   │   ├── model              # ORM 模型（Wuhan_Buildings / Wuhan_roads / Wuhan_events）
│   │   └── blueprints         # /api/Wuhan_* 与 /api/spatial 蓝图 + 统一错误处理
│   ├── data                   # 原始 GeoJSON 数据（入库来源）
│   ├── venv                   # 项目虚拟环境（不入库）
│   └── .env                   # 数据库连接等敏感配置（不入库）
└── frontend
    └── smart-city             # Vue 3 前端
        ├── vite.config.js     # /api 代理 → http://127.0.0.1:5000
        ├── .env               # Mapbox Access Token
        ├── .env.development   # VITE_API_BASE_URL（留空，走代理）
        └── src
            ├── main.js        # 应用入口
            ├── App.vue        # 根组件
            ├── api            # Axios 请求封装与接口定义
            ├── composables    # useSceneMap / useLayers / useEventBuffer / useBoxQuery
            ├── assets         # 图标、图片、样式
            └── components
                ├── MapContainer.vue   # Mapbox + L7 Scene 初始化（provide 共享场景）
                ├── MapControls.vue    # 地图控件
                ├── ScreenScale.vue    # 大屏等比缩放
                ├── LayerPanel         # 图层显隐面板
                ├── SmartCity          # 建筑 / 道路图层加载
                └── ScreenPanel        # 图表面板 + 底部工具栏（含缓冲区分析）
```

## 🚀 快速开始

### 环境要求

- Node.js ≥ 18（建议 20+）
- Python ≥ 3.9
- PostgreSQL ≥ 12，并启用 **PostGIS** 扩展

### 1. 准备数据库

```sql
CREATE DATABASE wuhan_smartcity;
-- 在该库中启用 PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
```

将数据库连接串写入 `backend/.env`：

```
DATABASE_URL=postgresql+psycopg2://用户:密码@主机:端口/库名
```

创建三张空间表（`Wuhan_Buildings` / `Wuhan_roads` / `Wuhan_events`，SRID 4326）并导入 `backend/data/*.json` 数据（可按需写脚本或手工导入）。

### 2. 启动后端

```bash
cd backend
# Windows 下务必使用项目虚拟环境中的解释器
venv\Scripts\python.exe run.py
# 或直接双击 run.bat
# 默认运行在 http://127.0.0.1:5000
```

> 后端依赖：flask、flask-smorest、flask-sqlalchemy、flask-migrate、flask-jwt-extended、geoalchemy2、psycopg2、shapely 等。

### 3. 启动前端

```bash
cd frontend/smart-city
npm install
npm run dev
```

打开终端输出的本地地址（默认 `http://localhost:5173`）即可访问。

> **注意**：前端依赖 Mapbox 底图，需保证 `frontend/smart-city/.env` 中的 `VITE_TOKEN` 有效。仓库内已内置示例 pk token，若失效请替换为自己的 Mapbox Access Token。

## 🔧 环境变量

| 文件 | 变量 | 说明 |
| --- | --- | --- |
| `frontend/smart-city/.env` | `VITE_TOKEN` | Mapbox 访问令牌（公开 pk token） |
| `frontend/smart-city/.env.development` | `VITE_API_BASE_URL` | 留空：与 dev server 同源，跨域由 Vite 代理处理 |
| `backend/.env` | `DATABASE_URL` | PostgreSQL 连接串（含凭据，**不入库**） |
| `backend/.env` | `SECRET_KEY` | JWT / 会话密钥（可选） |

> 生产环境建议在 Mapbox 后台为 token 配置 URL 白名单，避免被盗用。

## 📡 接口说明

所有接口均返回统一信封：`{ "code": 0, "msg": "success", "data": ... }`。
`data` 为 GeoJSON `FeatureCollection`（空间查询类）或普通对象（增删改类）。蓝图前缀均为 `/api`。

### 建筑数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/Wuhan_Buildings/` | 获取全部建筑（FeatureCollection） |
| GET | `/api/Wuhan_Buildings/<id>` | 按 id 获取单个建筑 |
| POST | `/api/Wuhan_Buildings/` | 新增建筑 |
| DELETE | `/api/Wuhan_Buildings/<id>` | 按 id 删除建筑 |

### 道路数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/Wuhan_roads/` | 获取全部道路（FeatureCollection） |
| GET | `/api/Wuhan_roads/<id>` | 按 id 获取单条道路 |
| POST | `/api/Wuhan_roads/` | 新增道路 |
| DELETE | `/api/Wuhan_roads/<id>` | 按 id 删除道路 |

### 交通事件数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/Wuhan_events/` | 获取全部事件（FeatureCollection） |
| GET | `/api/Wuhan_events/<id>` | 按 id 获取单个事件 |
| GET | `/api/Wuhan_events/<id>/buffer?distance=1000` | **缓冲区分析**：返回目标点缓冲区面 + 圈内其他事故点 |
| POST | `/api/Wuhan_events/` | 新增事件 |
| DELETE | `/api/Wuhan_events/<id>` | 按 id 删除事件 |

> 增删改操作实时写回 PostgreSQL；`buffer` 接口的 `distance` 为缓冲区半径（米，默认 1000，范围 1~50000）。

### 空间查询（bbox）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/spatial/bbox` | 按矩形范围查询要素，返回 FeatureCollection |

查询参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `minx` / `miny` | 是 | 矩形左下角经纬度 |
| `maxx` / `maxy` | 是 | 矩形右上角经纬度 |
| `layer` | 否 | `events`（默认）/ `roads` / `buildings` |
| `limit` | 否 | 返回条数上限，默认 1000，最大 5000 |

```bash
curl "http://127.0.0.1:5000/api/spatial/bbox?layer=events&minx=114.35&miny=30.45&maxx=114.45&maxy=30.55"
```

> 后端使用 `ST_MakeEnvelope(minx,miny,maxx,maxy,4326)` + `ST_Intersects` 在数据库侧过滤；
> 需满足 `minx < maxx` 且 `miny < maxy`，否则返回 400。

## 🗂️ 数据说明

- 空间数据存于 PostgreSQL / PostGIS，坐标系 SRID 4326：
  - **Wuhan_Buildings**：`Polygon`，属性 `Elevation` 用于建筑高度拉伸
  - **Wuhan_roads**：`LineString`，属性含 `osm_id`、`name`、`type`
  - **Wuhan_events**：`Point`，属性含 `id`（String）、`name`、`level`、`car_num`、`phone`、`event_num`、`area`
- `backend/data/*.json` 为原始 GeoJSON 文件，可作入库数据源。

## ⚠️ 注意事项

- **跨域**：不使用 CORS，开发环境由 Vite `server.proxy` 将 `/api` 转发到 `127.0.0.1:5000`。
- 前端 `request.js` 拦截器约定后端 `code === 0` 表示成功，非 0 时 reject（展示 `msg`）。
- `MapContainer.vue` 通过 `provide/inject`（`SCENE_MAP_KEY`）共享 L7 Scene 与 Mapbox Map 实例，需在 `MapContainer` 内使用 `useSceneMap`。
- 图层实例（L7 Layer）不要放进 Vue `reactive` / `ref`，避免代理破坏内部 `this` 指向（见 `useLayers.js` 注释）。
- 后端启动务必使用项目虚拟环境解释器（`backend/venv/Scripts/python.exe`），全局 Python 可能缺少依赖。
- `backend/.env`、`venv/`、`__pycache__/` 已在 `.gitignore` 中，**不会入库**。

## 📄 License

仅用于学习与演示。
