<template>
  <div class="login">
    <el-card>
      <el-form ref="loginForm" :model="loginForm" @submit.native.prevent="submitForm('loginForm')">
        <el-form-item label="Username" prop="username">
          <el-input v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="loginForm.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('loginForm')">Log in</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
   name: "LoginView",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios
            .post("/api/v1/token/", this.loginForm)
            .then((response) => {
              localStorage.setItem("access", response.data.access);
              localStorage.setItem("refresh", response.data.refresh);
              axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;
              this.$router.push("/"); // redirect to home page
            })
            .catch((error) => {
              if (error.response.data.detail === "Given token not valid for any token type") {
                this.refreshToken();
              } else {
                ElMessage.error("Неверное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.");
              }
            });
        }
      });
    },
    refreshToken() {
      axios
        .post("/api/v1/token/refresh/", { refresh: localStorage.getItem("refresh") })
        .then((response) => {
          localStorage.setItem("access", response.data.access);
          axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;
          this.submitForm("loginForm");
        })
        .catch((error) => {
          console.log(error);
          ElMessage.error("Session expired. Please log in again.");
          this.$router.push("/login");
        });
    },
  },
};
</script>

<style scoped>
.login {
  width: 400px;
  margin: 50px auto;
}
</style>