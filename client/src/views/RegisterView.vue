<template>
  <div class="register">
    <el-card>
      <el-form ref="registerForm" :model="registerForm" @submit.native.prevent="submitForm('registerForm')">
        <el-form-item label="Логин" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="Пароль" prop="password">
          <el-input type="password" v-model="registerForm.password"></el-input>
        </el-form-item>
        <el-form-item id="pass-confirm-label" label="Подтвердите пароль" prop="confirmPassword">
          <el-input type="password" v-model="registerForm.confirmPassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('registerForm')">Зарегистрироваться</el-button>
        </el-form-item>
      </el-form>

      <p class="login-cta">Уже есть аккаунт? <router-link to="/login">Войдите!</router-link></p>
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
  margin: 20% auto;
}

.login-cta {
  margin-top: 1rem;
  text-align: center;
}

:deep(.el-form-item__label) {
  width: 30%;
  text-align: right;
}

/*form > div:nth-child(4) label{*/
/*  line-height: 20px;*/
/*}*/

:deep(.el-button){
  margin: 1.8rem auto 0.8rem auto;
}

.login-cta a{
  color: #ff5555;
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.login-cta a:hover{
  color: #ff2f2f;
}
</style>


