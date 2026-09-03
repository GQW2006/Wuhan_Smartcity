// 导入axios
import axios from 'axios'

// 创建axios实例
// baseURL 为空: 与 dev server 同源, /api 接口由 vite-plugin-mock 拦截
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

// 配置响应拦截器
instance.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== 0) {
      console.log(res.msg)
      return Promise.reject(new Error(res.msg))
    }
    return res.data
  },
  (error) => {
    console.log(error)
    return Promise.reject(error)
  },
)

// 导出axios实例
export default instance
