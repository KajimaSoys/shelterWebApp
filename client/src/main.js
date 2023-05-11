import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/style.css'
import axios from "axios";

import ElementPlus from "element-plus";
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'


const app = createApp(App)

app.use(router, axios)

app.use(ElementPlus)

let backendURL = import.meta.env.VITE_BACKEND_HOST
axios.defaults.baseURL = backendURL

app.mount('#app')

app.provide('backendURL', backendURL)
