<template>
  <div class="shelter-list">
    <h1>Приюты для животных</h1>
    <el-input class="shelter-search" size="large" placeholder="Поиск..." v-model="searchText"></el-input>

    <div class="main-content">
      <div class="filters">
        <h2>Фильтры</h2>
        <!-- TODO Add filter components here -->
        <div style="color: gray">Скоро..</div>
      </div>
      <div class="shelters">
        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>

          <el-select v-model="perPage" placeholder="Кол-во записей" style="margin-left: 1rem; width: 4rem" title="Записей на странице">
            <el-option
              v-for="item in [10, 20, 50]"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>

        <el-card v-for="shelter in shelters" :key="shelter.id" @click="goToShelter(shelter.id)" class="shelter-card">
          <div class="shelter-card-image">
            <img v-if="shelter.photos.length > 0" :src="shelter.photos[0].photo">
            <img v-else src="/no-photo.gif">
          </div>
          <div class="shelter-card-content">
            <h2>{{ shelter.name }}</h2>

            <div class="shelter-card-info">
              <div><b>Адрес:</b> {{ shelter.city }}, {{ shelter.street }}{{ shelter.house !== '' ? `, ${shelter.house}`: ''}}</div>

              <div><b>Телефон: </b>
                <a :href="`tel:${shelter.phone_number}`" @click.stop>
                  {{ shelter.phone_number }}
                </a>
              </div>
              <div v-if="shelter.website_link !== ''">
                <b>Сайт: </b>
                <a :href="shelter.website_link" target="_blank" @click.stop>
                  {{ shelter.website_link }}
                </a>
              </div>
              <div><b>Email:</b> {{ shelter.email }}</div>

              <div v-html="shelter.description"></div>

              <div style="font-size: 14px">Рейтинг: {{ shelter.rating }}</div>
            </div>
          </div>
        </el-card>

        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>

          <el-select v-model="perPage" placeholder="Кол-во записей" style="margin-left: 1rem; width: 4rem" title="Записей на странице">
            <el-option
              v-for="item in [10, 20, 50]"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ShelterList",
  data() {
    return {
      shelters: [],
      searchText: '',
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
    };
  },
  methods: {
    getShelters() {
      // TODO Нужно запрашивать только основную информацию приютов, чтобы сэкономить время при запросе
      axios
        .get("/api/v1/shelters/", {
          params: {
            page: this.currentPage,
            per_page: this.perPage
          }
        })
        .then(response => {
          this.shelters = response.data.results;
          this.totalPages = response.data.total_pages;
        })
        .catch(error => {
          console.error(error);
        });
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getShelters();
        window.scrollTo(0, 0);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.getShelters();
        window.scrollTo(0, 0);
      }
    },
    changePerPage() {
      this.currentPage = 1;
      this.getShelters();
    },
    goToShelter(id) {
      this.$router.push(`/shelter/${id}`);
    },
  },
  watch: {
    perPage: {
      handler() {
        this.changePerPage();
      },
      immediate: true
    }
  },
  created() {
    this.getShelters();
  }
};
</script>

<style scoped>
.shelter-search{
  padding: 1rem 0;
}

.shelter-list {
  width: 80%;
  margin: 0 auto;
}
.main-content {
  display: flex;
  gap: 1em;
}
.filters {
  flex: 1;
  border-right: 1px solid #ccc;
  padding-right: 1em;
}
.shelters {
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

.shelter-card-image{
  width: 35%;
  flex-basis: 35%;
  display: flex;
}

.shelter-card-image img{
  width: 100%;
  object-fit: cover;
}

.shelter-card-content{
  width: 65%;
  flex-basis: 65%;
}

.shelter-card-content h2{
  margin-top: 0;
}

.shelter-card-info{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.shelter-card-info div{
  margin: 0.5rem 0;
}

.shelter-card-info a{
  color: var(--el-color-primary);
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.shelter-card-info a:hover{
  color: var(--el-color-primary-dark-1);
}

.pagination{
  margin: 2rem;
}
</style>