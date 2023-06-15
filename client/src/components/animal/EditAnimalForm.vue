<template>
  <div class="animal-edit">
    <h1>Редактировать животное</h1>
    <el-form
      :model="form"
      @submit.native.prevent="onSubmit"
      label-width="160px"
      :rules="rules"
      status-icon
      ref="animalDataRef"
    >
    <el-form-item label="Имя" prop="name">
      <el-input v-model="form.name" clearable placeholder="Введите имя животного"></el-input>
    </el-form-item>
    <el-form-item label="Тип животного" prop="animal_type">
      <el-input v-model="form.animal_type" clearable placeholder="Введите тип животного"></el-input>
    </el-form-item>
    <el-form-item label="Порода">
      <el-input v-model="form.breed" clearable placeholder="Введите породу"></el-input>
    </el-form-item>
    <el-form-item label="Возраст (месяцы)">
      <el-input v-model="form.age" clearable placeholder="Введите возраст в месяцах"></el-input>
    </el-form-item>
    <el-form-item label="Пол">
      <el-select v-model="form.gender" placeholder="Выберите пол">
        <el-option label="Самец" value="male"></el-option>
        <el-option label="Самка" value="female"></el-option>
        <el-option label="Неизвестно" value="unknown"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Вес (граммы)">
      <el-input v-model="form.weight" clearable placeholder="Введите вес в граммах"></el-input>
    </el-form-item>
    <el-form-item label="Состояние здоровья">
      <el-input v-model="form.health_status" clearable placeholder="Введите состояние здоровья"></el-input>
    </el-form-item>
    <el-form-item label="Описание">
      <el-input v-model="form.description" clearable type="textarea" :rows="3"></el-input>
    </el-form-item>
    <el-form-item label="Фото животного">
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
        <el-button slot="trigger" type="default">Выбрать</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item class="submit-button">
      <el-button type="primary" @click="onSubmit()">Сохранить</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";
import {ElNotification} from "element-plus";

export default {
  name: "EditAnimalForm",
  inject: ['backendURL'],
  data(){
    return{
      form: {},
      fileList: [],
      user: null,
      rules: {
        name: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        animal_type: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
      },
    }
  },
  computed: {
    uploadAction() {
      return `${this.backendURL}/api/v1/animal_photos/`;
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
        await this.getAnimalData();

        if (this.form.shelter_owner !== this.user){
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
    async getAnimalData() {
      try {
        const response = await axios.get(`/api/v1/animals/${this.$route.params.animalId}/`);
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
        await axios.delete(`/api/v1/animal_photos/${file.name}/`);
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
          formData.append('animal', this.$route.params.animalId);
          formData.append('photo', file.raw);
          try {
            await axios.post(`${this.backendURL}/api/v1/animal_photos/`, formData, {
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
      this.$refs.animalDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;

          let formData = new FormData();

          for (let key in this.form) {
            formData.append(key, this.form[key]);
          }

          try {
            const response = await axios.put(`/api/v1/animals/${this.$route.params.animalId}/`, formData);
            console.log(response.data);
            if (response.data) {
              await this.uploadPhotos();
            }
            this.$router.push(`/shelter/${this.$route.params.id}`)
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
.animal-edit {
  width: 80%;
  margin: 0 auto;
  position: relative;
}
.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>