<template>
  <div class="register">
    <el-card>
      <el-form ref="registerForm" :model="registerForm" @submit.native.prevent="submitForm('registerForm')">
        <el-form-item label="Username" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="registerForm.password"></el-input>
        </el-form-item>
        <el-form-item label="Confirm Password" prop="confirmPassword">
          <el-input type="password" v-model="registerForm.confirmPassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('registerForm')">Register</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  name: "RegisterView",
  data() {
    return {
      registerForm: {
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.registerForm.password !== this.registerForm.confirmPassword) {
            ElMessage.error("Пароли не совпадают. Повторите попытку.");
            return;
          }
          axios
            .post("/api/v1/register/", this.registerForm)
            .then(() => {
              ElMessage.success("Регистрация прошла успешно. Пожалуйста, авторизуйтесь.");
              this.$router.push("/login"); // redirect to login page
            })
            .catch((error) => {
              console.log(error);
              ElMessage.error("Произошла ошибка. Попробуйте еще раз.");
            });
        }
      });
    }
  }
};
</script>

<style scoped>
.register {
  width: 400px;
  margin: 50px auto;
}
</style>


