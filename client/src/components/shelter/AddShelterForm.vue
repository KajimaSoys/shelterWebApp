<template>
  <div class="shelter-add">
    <h1>Добавить приют для животных</h1>
    <el-form
      :model="form"
      @submit.native.prevent="onSubmit"
      label-width="120px"
      :rules="rules"

      status-icon
      ref="shelterDataRef"
  >
    <el-form-item label="Название" prop="name">
      <el-input
          v-model="form.name"
          clearable
          placeholder="Введите название Вашего приюта"
      ></el-input>
    </el-form-item>

    <el-form-item label="Описание">
      <el-input
          v-model="form.description"
          clearable
          type="textarea"
          :rows="3"
      ></el-input>
    </el-form-item>

    <el-form-item label="Город" prop="city">
      <el-input
          v-model="form.city"
          clearable
          placeholder="Казань"
      ></el-input>
    </el-form-item>

    <el-form-item label="Улица" prop="street">
      <el-input
          v-model="form.street"
          clearable
          placeholder="Первая"
      ></el-input>
    </el-form-item>

    <el-form-item label="Дом">
      <el-input
          v-model="form.house"
          clearable
          placeholder="1"
      ></el-input>
    </el-form-item>

    <el-form-item label="Дополнительная информация" class="add-info-field">
      <el-input
          v-model="form.additional_info"
          clearable
          type="textarea"
          :rows="3"
      ></el-input>
    </el-form-item>

    <el-form-item label="Сайт">
      <el-input
          v-model="form.website_link"
          clearable
          placeholder="https://yoursite.com"
      ></el-input>
    </el-form-item>

    <el-form-item label="Instagram">
      <el-input
          v-model="form.instagram_link"
          clearable
      ></el-input>
    </el-form-item>

    <el-form-item label="Telegram">
      <el-input
          v-model="form.telegram_link"
          clearable
      ></el-input>
    </el-form-item>

    <el-form-item label="ВКонтакте">
      <el-input
          v-model="form.vk_link"
          clearable
      ></el-input>
    </el-form-item>

    <el-form-item label="Телефон" prop="phone_number">
      <el-input
          v-model="form.phone_number"
          clearable
          placeholder="+7 (___) ___-__-__"
          v-mask="'+7 (###) ###-##-##'"
      ></el-input>
    </el-form-item>

    <el-form-item label="Email" prop="email">
      <el-input
          v-model="form.email"
          clearable
          placeholder="yourmail@mail.ru"
      ></el-input>
    </el-form-item>


    <el-form-item class="submit-button">
      <el-button type="primary" @click="onSubmit">Отправить на проверку</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";
import {mask} from 'vue-the-mask'

export default {
  name: "AddShelterForm",
  directives: {mask},
  data() {
    return {
      form: {
        name: '',
        description: '',
        city: '',
        street: '',
        house: '',
        additional_info: '',
        website_link: '',
        instagram_link: '',
        telegram_link: '',
        vk_link: '',
        phone_number: '',
        email: '',
      },
      rules: {
        name: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        city: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        street: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        phone_number: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        email: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
      },
    }
  },
  created() {
    if (!localStorage.getItem('access')) {
      this.$router.push('/login') // or whatever your login route is
    } else {
      this.form.owner = this.getOwnerId();
    }
  },
  methods: {
    async getUserDetails() {
      axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;
      try {
        const response = await axios.get('/api/v1/user-details/');
        return response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.getUserDetails();
        }
        console.log(error);
      }
    },
    async getOwnerId() {
      const userDetails = await this.getUserDetails();
      return userDetails ? userDetails.id : null;
    },
    async onSubmit() {
      this.$refs.shelterDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;
          try {
            const response = await axios.post('/api/v1/shelters/', this.form);
            console.log(response.data);
            this.$router.push('/shelters')
          } catch (error) {
            if (error.response && error.response.status === 401) {
              await this.$refreshToken();
              return this.onSubmit();
            }
            console.log(error);
          }
        } else {
          console.log('Form validation failed!');
          return false;
        }
      });
    }
  }
}
</script>

<style scoped>
.shelter-add {
  width: 80%;
  margin: 0 auto;
  position: relative;
}

.add-info-field{
  text-align: right;
}

.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>