<template>
  <div class="reports-list" v-if="moneyReports.length > 0">
    <h1>Расходы на уход за животными</h1>
    <div class="report-manage-buttons" v-if="owner">
      <el-button type="primary" @click="addReport">Добавить отчет</el-button>
    </div>

    <div class="main-content">
      <div class="reports">
        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>
        </div>

        <el-card v-for="report in paginatedMoneyReports" :key="report.id" class="animal-card">
          <div class="report-card-image">
            <img :src="report.photo ? report.photo : '/no-photo.gif'">
          </div>

          <div class="report-card-content">
            <h2 class="report-card-title">
              {{ report.title }}
              <el-button v-if="owner"  @click.stop="editReport(report.shelter, report.id)">
                <el-icon>
                  <Edit />
                </el-icon>
              </el-button>
              <el-button v-if="owner" @click.stop="deleteReport(report.id)">
                <el-icon>
                  <Delete />
                </el-icon>
              </el-button>
            </h2>
            <div class="report-card-info">
              <div>{{ report.description }}</div>
              <div>Cумма: {{ report.amount_spent }} руб.</div>
            </div>

          </div>
        </el-card>

        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>
        </div>
      </div>

    </div>
  </div>

  <div class="reports-list" v-else style="margin-bottom: 5rem">
    <h1>Приют пока не предоставил информацию о расходах..</h1>
    <div v-if="owner">
      <el-button type="primary" @click="addReport">Добавить отчет</el-button>
    </div>
  </div>
</template>

<script>
import {Delete, Edit} from "@element-plus/icons-vue";
import axios from "axios";
import {ElNotification} from "element-plus";

export default {
  name: "FundsSpent",
  props: {
    moneyReports: {
      type: Array,
      required: true
    },
    owner: {},
  },
  components: {
    Delete,
    Edit,
  },
  emits: [
    'reFetchShelter',
  ],
  data(){
    return{
      currentPage: 1,
      perPage: 10,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.moneyReports.length / this.perPage);
    },
    paginatedMoneyReports() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = this.currentPage * this.perPage;
      return this.moneyReports.slice(start, end);
    }
  },
  methods: {
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    addReport(){
      this.$router.push(`/shelter/${this.$route.params.id}/funds/add`);
    },
    editReport(id, reportId) {
      this.$router.push(`/shelter/${id}/funds/${reportId}/edit`);
    },
    async deleteReport(reportId) {
      try {
        await this.$confirm('Вы действительно хотите удалить отчет?', 'Внимание', {
          confirmButtonText: 'Да',
          cancelButtonText: 'Нет',
          type: 'warning'
        });
        await axios.delete(`/api/v1/money_reports/${reportId}/`);
        this.$emit('reFetchShelter')
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.deleteShelter(reportId);
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при удалении отчета',
            type: 'error',
          });
        }
      }
    },
  }
}
</script>

<style scoped>
.report-manage-buttons {
  position: absolute;
  right: 0;
  top: 10px;
}

.reports-list {
  width: 80%;
  margin: 5rem auto 0;
  position: relative;
}
.main-content {
  display: flex;
  gap: 1em;
}
.reports {
  flex: 3;
}

.el-card {
  cursor: pointer;
  padding: 1em;
  margin-bottom: 1em;
  transition: transform 0.3s ease;

}

.el-card:hover {
  transform: scale(1.03);
}

:deep(.el-card__body){
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.report-card-image{
  width: 35%;
  flex-basis: 35%;
  display: flex;
}

.report-card-image img{
  width: 100%;
  object-fit: cover;
}

.report-card-content{
  width: 65%;
  flex-basis: 65%;
}

.report-card-content h2{
  margin-top: 0;
}

.report-card-info{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.report-card-info div{
  margin: 0.5rem 0;
}

.report-card-info a{
  color: var(--el-color-primary);
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.report-card-info a:hover{
  color: var(--el-color-primary-dark-1);
}

.pagination{
  margin: 2rem;
}
</style>