<template>
  <div class="money-report-add">
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
        ref="upload"
        :limit="1"
        :on-exceed="handleExceed"
      >
        <el-button slot="trigger" size="small" type="default">Выбрать</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item class="submit-button">
      <el-button type="default" @click="onSubmit(true)">Отправить и добавить другой отчет</el-button>
      <el-button type="primary" @click="onSubmit(false)">Отправить</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "axios";
import { genFileId } from 'element-plus'

export default {
  name: "AddFundraisingForm",
  inject: ['backendURL'],

  data(){
    return{
      form: {
        title: '',
        description: '',
        amount_spent: '',
        photo: null,
        shelter: '',
      },
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
    if (!localStorage.getItem('access')) {
      this.$router.push('/login')
    } else {
      this.form.shelter = this.$route.params.id;
    }
  },
  methods: {
    handlePhotoChange(file) {
      this.form.photo = file.raw;
      console.log(this.form.photo)
    },
    handleExceed(files) {
      this.$refs.upload.clearFiles();
      const file = files[0];
      file.uid = genFileId();
      this.$refs.upload.handleStart(file);
    },
    async onSubmit(addOtherReport) {
      this.$refs.moneyReportDataRef.validate(async (valid) => {
        if (valid) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('access')}`;

          let formData = new FormData();

          for (let key in this.form) {
            formData.append(key, this.form[key]);
          }

          try {
            const response = await axios.post(`${this.backendURL}/api/v1/money_reports/`, formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              }
            });
            console.log(response.data);
            if (addOtherReport){
              this.form = {
                title: '',
                description: '',
                amount_spent: '',
                photo: null,
                shelter: this.$route.params.id
              }
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
  }
}
</script>

<style scoped>
.money-report-add {
  width: 80%;
  margin: 0 auto;
  position: relative;
}
.submit-button{
  flex-direction: column;
  align-items: flex-end;
}
</style>