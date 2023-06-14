<template>
  <div class="reports-list" v-if="moneyReports.length > 0">
    <h1>Расходы на уход за животными</h1>
    <div class="report-manage-buttons">
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
            <h2 class="animal-card-title">{{ report.title }}</h2>
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
    <div>
      <el-button type="primary" @click="addReport">Добавить отчет</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "FundsSpent",
  props: {
    moneyReports: {
      type: Array,
      required: true
    }
  },
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