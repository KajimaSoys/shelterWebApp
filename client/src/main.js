import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/style.css'
import axios from "axios";

import ElementPlus, {ElMessage} from "element-plus";
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'


const app = createApp(App)
app.use(router, axios)
app.use(ElementPlus)
let backendURL = import.meta.env.VITE_BACKEND_HOST;
axios.defaults.baseURL = backendURL
app.mount('#app')
app.provide('backendURL', backendURL)

app.config.globalProperties.$refreshToken = async function () {
    await axios
        .post("/api/v1/token/refresh/", { refresh: localStorage.getItem("refresh") })
        .then((response) => {
          localStorage.setItem("access", response.data.access);
          axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;
        })
        .catch((error) => {
          console.log(error);
          ElMessage.error("Session expired. Please log in again.");
        });
};
