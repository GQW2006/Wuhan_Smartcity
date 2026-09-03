import { createApp } from 'vue'
import App from './App.vue'


// 导入初始化样式
import './assets/styles/reset.css'

// 配置 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

createApp(App).use(ElementPlus).mount('#app')