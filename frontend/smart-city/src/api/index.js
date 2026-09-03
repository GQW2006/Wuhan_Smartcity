// 导入request实例
import request from './request'

// 编写接口

// 获取城市建筑数据
export const getCityBuildings = () => {
  return request({
    url: '/Wuhan_Buildings/',
    method: 'GET',
  })
}

// 获取道路数据
export const getRoads = () => {
  return request({
    url: '/Wuhan_roads/',
    method: 'GET',
  })
}

// 获取交通事件数据
export const getEvents = () => {
  return request({
    url: '/Wuhan_events/',
    method: 'GET',
  })
}