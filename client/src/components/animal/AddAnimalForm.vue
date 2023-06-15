<template>
  <div class="animal-add">
    <h1>Добавить животное</h1>
    <el-form
      :model="form"
      @submit.native.prevent="onSubmit"
      label-width="260px"
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

    <el-form-item label="Статус животного">
      <el-select v-model="form.status" placeholder="Выберите текущий статус животного">
        <el-option label="В приюте" value="in_shelter"></el-option>
        <el-option label="Приютили" value="adopted"></el-option>
        <el-option label="Отсутствует" value="missing"></el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="Начало пребывания в приюте">
      <el-date-picker
        v-model="form.created_at"
        type="date"
        placeholder="Выберите день"
        :disabled-date="disabledDate"
        :shortcuts="shortcuts"
        value-format="DD.MM.YYYY"
        format="DD.MM.YYYY"
      />
    </el-form-item>

    <el-form-item label="Окончание пребывания в приюте">
      <el-date-picker
        v-model="form.left_at"
        type="date"
        placeholder="Выберите день"
        :disabled-date="disabledDate"
        :shortcuts="shortcuts"
        value-format="DD.MM.YYYY"
        format="DD.MM.YYYY"
      />
    </el-form-item>

    <el-form-item label="Фото животного">
      <el-upload
        :action="uploadAction"
        multiple
        :auto-upload="false"
        :on-change="handlePhotosChange"
        :file-list="fileList"
        :headers="headers"
        ref="upload"
      >
        <el-button slot="trigger" size="small" type="default">Выбрать</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item class="submit-button">
      <el-button type="default" @click="onSubmit(true)">Отправить и добавить другое животное</el-button>
      <el-button type="primary" @click="onSubmit(false)">Отправить</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddAnimalForm",
  inject: ['backendURL'],

  data(){
    return{
      form: {
        name: '',
        animal_type: '',
        breed: '',
        age: '',
        gender: 'unknown',
        weight: '',
        health_status: '',
        description: '',
        status: 'in_shelter',
        created_at: new Date().toLocaleDateString(),
        left_at: null,
      },
      fileList: [],
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
      shortcuts: [
        {
          text: 'Сегодня',
          value: new Date(),
        },
        {
          text: 'Вчера',
          value: () => {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            return date
          },
        },
        {
          text: 'Неделю назад',
          value: () => {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            return date
          },
        },
      ]
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
    if (!localStorage.getItem('access')) {
      this.$router.push('/login')
    } else {
      this.form.shelter = this.$route.params.id;
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
    handlePhotosChange(file, fileList) {
      this.fileList = fileList;
    },
    submitUpload() {
      this.$refs.upload.submit();
    },
    async onSubmit(addOtherAnimal) {
      this.$refs.animalDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;

          let formData = new FormData();

          const transformDate = (dateStr) => {
            const parts = dateStr.split(".");
            return new Date(parts[2], parts[1] - 1, parts[0]).toISOString().split('T')[0];
          }

          for (let key in this.form) {
            if (this.form[key] !== null) {
              if (key === 'created_at' || key === 'left_at') {
                formData.append(key, transformDate(this.form[key]));
              } else {
                formData.append(key, this.form[key]);
              }
            }
          }

          try {
            const response = await axios.post('/api/v1/animals/', formData);
            console.log(response.data);
            if (response.data) {
              await this.uploadPhotos(response.data.id);
            }
            if (addOtherAnimal){
              this.form = {
                name: '',
                animal_type: '',
                breed: '',
                age: '',
                gender: 'unknown',
                weight: '',
                health_status: '',
                description: '',
                status: 'in_shelter',
                created_at: '',
                left_at: '',
                shelter: this.$route.params.id
              }
              this.fileList = []
            }
            else {
              this.$router.push(`/shelter/${this.$route.params.id}`)
            }
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

    async uploadPhotos(animalId) {
      for (let file of this.fileList) {
        let formData = new FormData();

        formData.append('animal', animalId);
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
    },
    disabledDate: (time) => {
      return time.getTime() > Date.now();
    }
  }
}
</script>

<style scoped>
.animal-add {
  width: 80%;
  margin: 0 auto;
  position: relative;
}
.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>