<template>
  <div class="animal-list" v-if="animals.length > 0">
    <h1>Животные приюта</h1>
    <div class="animal-manage-buttons">
      <el-button type="primary" @click="addAnimal">Добавить животное</el-button>
    </div>

    <el-input class="animal-search" size="large" placeholder="Поиск.." v-model="searchText" clearable></el-input>

    <div class="main-content">
      <div class="filters">
        <h2>Фильтры</h2>
        <!-- Animal Type Filter -->
        <div>
          <label class="filter-label">Тип животного:</label>
          <div style="margin-top: 1rem">
            <el-select v-model="selectedAnimalType" placeholder="Выберите животное" clearable>
              <el-option
                v-for="type in animalTypeList"
                :key="type"
                :label="type"
                :value="type">
              </el-option>
            </el-select>
          </div>
        </div>

        <!-- Breed Filter -->
        <div>
          <label class="filter-label">Порода:</label>
          <div style="margin-top: 1rem">
            <el-select v-model="selectedBreed" placeholder="Выберите породу" clearable>
              <el-option
                v-for="breed in breedList"
                :key="breed"
                :label="breed"
                :value="breed">
              </el-option>
            </el-select>
          </div>
        </div>

        <!-- Gender Filter -->
        <div>
          <label class="filter-label">Пол:</label>
          <div style="margin-top: 1rem">
            <el-select v-model="selectedGender" placeholder="Выберите пол" clearable>
              <el-option
                v-for="gender in genderList"
                :key="gender"
                :label="genderChoices[gender]"
                :value="gender">
              </el-option>
            </el-select>
          </div>
        </div>

<!--        <el-button type="primary" @click="getAnimals">Apply</el-button>-->
      </div>

      <div class="animals" v-if="paginatedAnimals.length">
        <div class="pagination">
          <el-button @click="prevPage" :disabled="currentPage === 1">Предыдущая</el-button>
          <el-button disabled>{{ currentPage }}</el-button>
          <el-button @click="nextPage" :disabled="currentPage === totalPages">Следующая</el-button>
        </div>

        <el-card v-for="animal in paginatedAnimals" :key="animal.id" @click="goToAnimal(animal.shelter, animal.id)" class="animal-card">
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
      <div v-else class="animals">
        Животные не найдены. Попробуйте изменить критерии поиска.
      </div>
    </div>
  </div>

  <div class="animal-list" v-else>
    <h1>Приют пока не добавил животных..</h1>
    <div>
      <el-button type="primary" @click="addAnimal">Добавить животное</el-button>
    </div>
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
      selectedAnimalType: '',
      selectedBreed: '',
      selectedGender: '',

      genderChoices: {
        'male': 'Самец',
        'female': 'Самка',
        'unknown': 'Неизвестно',
      }
    };
  },
  computed: {
    filteredAnimals() {
      let result = this.animals;

      if (this.searchText) {
        result = result.filter(animal => animal.name.toLowerCase().includes(this.searchText.toLowerCase()));
      }

      if (this.selectedAnimalType) {
        result = result.filter(animal => animal.animal_type === this.selectedAnimalType);
      }

      if (this.selectedBreed) {
        result = result.filter(animal => animal.breed === this.selectedBreed);
      }

      if (this.selectedGender) {
        result = result.filter(animal => animal.gender === this.selectedGender);
      }

      return result;
    },
    animalTypeList() {
      return [...new Set(this.animals.map(animal => animal.animal_type))];
    },
    breedList() {
      return [...new Set(this.animals.map(animal => animal.breed).filter(Boolean))];
    },
    genderList() {
      return [...new Set(this.animals.map(animal => animal.gender))];
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
    goToAnimal(id, animalId) {
      this.$router.push(`/shelter/${id}/animal/${animalId}`);
    },
    addAnimal(){
      this.$router.push(`/shelter/${this.$route.params.id}/animal/add`);
    }
  },
};
</script>

<style scoped>
.animal-manage-buttons {
  position: absolute;
  right: 0;
  top: 10px;
}

.animal-search{
  padding: 1rem 0;
}

.animal-list {
  width: 80%;
  margin: 5rem auto 0;
  position: relative;
}
.main-content {
  display: flex;
  gap: 1em;
}
.filters {
  flex: 1;
  border-right: 1px solid #ccc;
  padding-right: 1em;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: 5rem;
  margin-bottom: 1rem;
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