<template>
  <div class="money-report-edit">
    <h1>Добавить отчет о расходах</h1>
    <el-form
      :model="form"
      @submit.native.prevent="onSubmit"
      label-width="180px"
      :rules="rules"
      status-icon
      ref="moneyReportDataRef"
    >
    <el-form-item label="Название" prop="title">
      <el-input v-model="form.title" clearable placeholder="Введите название для отчета"></el-input>
    </el-form-item>
    <el-form-item label="Описание">
      <el-input v-model="form.description" clearable type="textarea" :rows="3"></el-input>
    </el-form-item>
    <el-form-item label="Потраченная сумма" prop="amount_spent">
      <el-input v-model="form.amount_spent" clearable placeholder="Введите потраченную сумму"></el-input>
    </el-form-item>
    <el-form-item label="Фото отчета">
      <el-upload
        :auto-upload="false"
        :on-change="handlePhotoChange"
        :on-remove="handlePhotoRemove"
        ref="upload"
        :limit="1"
        :on-exceed="handleExceed"
        :file-list="fileList"
      >
        <el-button slot="trigger" size="small" type="default">Выбрать</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item class="submit-button">
      <el-button type="primary" @click="onSubmit()">Отправить</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";
import {ElNotification, genFileId} from 'element-plus'

export default {
  name: "EditFundraisingForm",
  inject: ['backendURL'],

  data(){
    return{
      form: {},
      fileList: [],
      rules: {
        title: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
        amount_spent: {
          required: true,
          message: "Поле обязательно для заполнения",
          trigger: "blur",
        },
      },
    }
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
        await this.getReportData();

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
    async getReportData() {
      try {
        const response = await axios.get(`/api/v1/money_reports/${this.$route.params.reportId}/`);
        this.form = response.data;
        if (response.data.photo) {
          this.fileList = [{
            name: response.data.photo.split('/').pop(),
            url: response.data.photo,
            status: 'success',
          }];
        }
      } catch (error) {
        if (error.response && error.response.status === 400) {
          ElNotification({
            title: 'Ошибка!',
            message: `Произошла ошибка при запросе: ${JSON.stringify(error.response.data)}`,
            type: 'error',
          });
        }
        console.log(error);
      }
    },

    handlePhotoChange(file) {
      this.form.photo = file.raw;
      console.log(this.form.photo)
    },
    handlePhotoRemove(){
      this.form.photo = ""
    },
    handleExceed(files) {
      this.$refs.upload.clearFiles();
      const file = files[0];
      file.uid = genFileId();
      this.$refs.upload.handleStart(file);
    },

    // handlePhotoRemove(file) {
    //   if (!file.isNew) {
    //     this.deletePhoto(file);
    //   } else {
    //     this.fileList = this.fileList.filter(f => f !== file);
    //   }
    // },
    async onSubmit() {
      this.$refs.moneyReportDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;

          let formData = new FormData();

          for (let key in this.form) {
            if(key === 'photo' && !(this.form[key] instanceof File) && (this.form[key] !== "")) {
              continue;
            }
            formData.append(key, this.form[key]);
          }

          try {
            const response = await axios.put(`/api/v1/money_reports/${this.$route.params.reportId}/`, formData);
            console.log(response.data);
            this.$router.push(`/shelter/${this.$route.params.id}`)
          } catch (error) {
            if (error.response && error.response.status === 401) {
              await this.$refreshToken();
              return this.onSubmit();
            }
            if (error.response && error.response.status === 400) {
              ElNotification({
                title: 'Ошибка!',
                message: `Произошла ошибка при запросе: ${JSON.stringify(error.response.data)}`,
                type: 'error',
              });
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
.money-report-edit {
  width: 80%;
  margin: 0 auto;
  position: relative;
}
.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>