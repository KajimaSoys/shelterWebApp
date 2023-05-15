<template>
  <div class="animal-list" v-if="animals.length > 0">
    <h1>Животные приюта</h1>
    <el-input class="animal-search" size="large" placeholder="Поиск.." v-model="searchText"></el-input>

    <div class="main-content">
      <div class="filters">
        <h2>Фильтры</h2>
        <!-- TODO Add filter components here -->
        <div style="color: gray">Скоро..</div>
      </div>

      <div class="animals">
        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>
        </div>

        <el-card v-for="animal in paginatedAnimals" :key="animal.id" class="animal-card">
          <div class="animal-card-image">
            <img :src="animal.photos.length > 0 ? animal.photos[0].photo : '/no-photo.gif'">
          </div>

          <div class="animal-card-content">
            <h2 class="animal-card-title">{{ animal.name }}</h2>
            <div class="animal-card-info">
              <div>Вид: {{ animal.animal_type }}</div>
              <div>Порода: {{ animal.breed }}</div>
              <div>Возраст (месцяцы): {{ animal.age }}</div>
              <div>Пол: {{ animal.gender }}</div>
              <div>Состояние здоровья: {{ animal.health_status }}</div>
              <div v-html="animal.description"></div>
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

  <div class="animal-list" v-else>
    <h1>Приют пока не добавил животных..</h1>
  </div>
</template>

<script>
export default {
  name: "AnimalList",
  props: {
    animals: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      searchText: '',
      currentPage: 1,
      perPage: 10,
    };
  },
  computed: {
    filteredAnimals() {
      if (!this.searchText) return this.animals;
      return this.animals.filter(animal => animal.name.toLowerCase().includes(this.searchText.toLowerCase()));
    },
    totalPages() {
      return Math.ceil(this.filteredAnimals.length / this.perPage);
    },
    paginatedAnimals() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = this.currentPage * this.perPage;
      return this.filteredAnimals.slice(start, end);
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
  },
};
</script>

<style scoped>
.animal-search{
  padding: 1rem 0;
}

.animal-list {
  width: 80%;
  margin: 5rem auto 0;
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
.animals {
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

.animal-card-image{
  width: 35%;
  flex-basis: 35%;
  display: flex;
}

.animal-card-image img{
  width: 100%;
  object-fit: cover;
}

.animal-card-content{
  width: 65%;
  flex-basis: 65%;
}

.animal-card-content h2{
  margin-top: 0;
}

.animal-card-info{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.animal-card-info div{
  margin: 0.5rem 0;
}

.animal-card-info a{
  color: var(--el-color-primary);
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.animal-card-info a:hover{
  color: var(--el-color-primary-dark-1);
}

.pagination{
  margin: 2rem;
}
</style>