<template>
  <div class="shelter-edit">
    <h1>Изменить приют "{{ form.name }}"</h1>
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

    <el-form-item label="Дополнительная информация" class="edit-info-field">
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

    <el-form-item label="Фото приюта" >
      <el-upload
        :action="uploadAction"
        multiple
        :auto-upload="false"
        :on-change="handlePhotosChange"
        :on-remove="handlePhotosRemove"
        :file-list="fileList"
        :headers="headers"
        ref="upload"
      >
        <el-button slot="trigger"  type="default">Выбрать</el-button>
      </el-upload>
    </el-form-item>


    <el-form-item class="submit-button">
      <el-button type="primary" @click="onSubmit">Сохранить</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";
import {mask} from 'vue-the-mask'
import {ElNotification} from "element-plus";

export default {
  name: "EditShelterForm",
  directives: {mask},
  inject: ['backendURL'],
  props: ['shelterId'],
  data() {
    return {
      form: {},
      fileList: [],
      user: null,
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
  computed: {
    uploadAction() {
      return `${this.backendURL}/api/v1/shelter_photos/`;
    },
    headers() {
      return {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      };
    },
  },
  created() {
    this.init()
  },
  methods: {
    async init() {
      if (!localStorage.getItem('access')) {
        this.$router.push('/login');
      } else {
        this.user = await this.getOwnerId();
        await this.getShelterData();

        if (this.form.owner !== this.user){
        this.$router.push('/shelters/');
          ElNotification({
            title: 'Ошибка!',
            message: 'Доступ запрещен',
            type: 'error',
          });
        }
      }
    },
    async getOwnerId() {
      const userDetails = await this.getUserDetails();
      return userDetails ? userDetails.id : null;
    },
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
    async getShelterData() {
      try {
        const response = await axios.get(`/api/v1/shelters/${this.$route.params.id}/`);
        this.form = response.data;
        this.fileList = response.data.photos.map(photo => ({
          url: photo.photo,
          name: photo.id,
          isNew: false,
        }));
      } catch (error) {
        console.log(error);
      }
    },

    handlePhotosRemove(file) {
      if (!file.isNew) {
        this.deletePhoto(file);
      } else {
        this.fileList = this.fileList.filter(f => f !== file);
      }
    },

    async deletePhoto(file) {
      try {
        await axios.delete(`/api/v1/shelter_photos/${file.name}/`);
        this.fileList = this.fileList.filter(f => f !== file);
      } catch (error) {
        console.log(error);
      }
    },

    handlePhotosChange(file, fileList) {
      fileList = fileList.map(file => ({
        ...file,
        isNew: file.isNew === undefined ? true : file.isNew,
        url: file.url || 'default-url'
      }));
      this.fileList = fileList;
    },
    async uploadPhotos() {
      for (let file of this.fileList) {
        console.log(file)
        if (file.isNew) {
          let formData = new FormData();
          formData.append('shelter', this.$route.params.id);
          formData.append('photo', file.raw);
          try {
            await axios.post(`${this.backendURL}/api/v1/shelter_photos/`, formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${localStorage.getItem('access')}`,
              }
            });
          } catch (error) {
            console.log(error);
          }
        }
      }
    },
    async onSubmit() {
      this.$refs.shelterDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;

          let formData = new FormData();

          for (let key in this.form) {
            formData.append(key, this.form[key]);
          }

          try {
            const response = await axios.put(`/api/v1/shelters/${this.$route.params.id}/`, formData);
            console.log(response.data);
            if (response.data) {
              await this.uploadPhotos();
            }
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
    },
  }
}
</script>

<style scoped>
.shelter-edit {
  width: 80%;
  margin: 0 auto;
  position: relative;
}

.edit-info-field{
  text-align: right;
}

.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>