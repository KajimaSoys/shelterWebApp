<template>
  <el-header class="header">
    <router-link to="/" class="logo">
      <img src="/ShelterCare.svg" alt="ShelterCare Logo" />
    </router-link>

    <div class="center-content">
      <!-- TODO Добавить меню -->
    </div>

    <div class="right-content">
      <el-button v-if="!isAuthenticated" type="link" @click="goToLogin">Войти</el-button>
      <div v-else>
        <span class="username">{{ username }}</span>
        <el-button type="default" effect="plain" disabled @click="goToAccount">Мой аккаунт</el-button>
        <el-button type="default" effect="plain" @click="logout">Выйти</el-button>
      </div>
    </div>
  </el-header>
</template>

<script>
import { ElMessage } from "element-plus";
import axios from "axios";

export default {
  name: "Navbar",
  data() {
    return {
      isAuthenticated: false,
      username: "",
    };
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem("access");
    this.username = localStorage.getItem("username");
  },
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    goToAccount() {
      // to be implemented
    },
    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("username");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push("/login");
      ElMessage.success("Вы успешно вышли из системы.");
    },
  },
};
</script>

<style scoped>
.header {
  width: 100%;
  height: 10vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  /*background-color: #000;*/
  z-index: 1000;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(4px) brightness(80%);
}

.logo {
  margin: 0 2rem;
}

.logo img {
  height: 40px;
}

.username {
  margin-right: 20px;
}
</style>