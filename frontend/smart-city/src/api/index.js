// 导入request实例
import request from './request'

// 编写接口

// 获取城市建筑数据
export const getCityBuildings = () => {
  return request({
    url: '/api/Wuhan_Buildings/',
    method: 'GET',
  })
}

// 获取道路数据
export const getRoads = () => {
  return request({
    url: '/api/Wuhan_roads/',
    method: 'GET',
  })
}

// 获取交通事件数据
export const getEvents = () => {
  return request({
    url: '/api/Wuhan_events/',
    method: 'GET',
  })
}

// 获取事故点缓冲区分析结果（后端 ST_Buffer 计算，distance 为半径米）
export const getEventBuffer = (id, distance = 1000) => {
  return request({
    url: `/api/Wuhan_events/${id}/buffer`,
    method: 'GET',
    params: { distance },
  })
}

// bbox 空间查询（后端 PostGIS ST_MakeEnvelope + ST_Intersects，返回 GeoJSON）
export const getSpatialByBbox = ({ layer = 'events', bbox, limit = 1000 }) => {
  const [minx, miny, maxx, maxy] = bbox
  return request({
    url: '/api/spatial/bbox',
    method: 'GET',
    params: { layer, minx, miny, maxx, maxy, limit },
  })
}