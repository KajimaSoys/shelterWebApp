<template>
  <div class="shelter-list">
    <h1>Приюты для животных</h1>
    <div  v-if="isAuthenticated" class="shelter-manage-buttons">
      <!-- TODO add my shelter page -->
<!--      <el-button type="default" @click="getShelters">Мои приюты</el-button>-->
      <el-button type="primary" @click="addShelter">Добавить приют</el-button>
    </div>
    <el-input class="shelter-search" size="large" placeholder="Поиск..." v-model="searchText" @input="debouncedGetShelters" clearable></el-input>

    <div class="main-content">
      <div class="filters">
        <h2>Фильтры</h2>

      <!-- Фильтр города -->
        <div>
          <label class="filter-label">Город:</label>
          <div style="margin-top: 1rem">
            <el-select v-model="selectedCity" placeholder="Выберите город" clearable>
              <el-option
                v-for="city in cities"
                :key="city"
                :label="city"
                :value="city">
              </el-option>
            </el-select>
          </div>
        </div>

      <!-- Фильтр по рейтингу -->
        <div>
          <label class="filter-label">Рейтинг:</label>
          <el-slider
            v-model="selectedRating"
            :min="0"
            :max="5"
            range
          >
          </el-slider>
        </div>

        <el-button type="primary" @click="getShelters">Применить</el-button>
      </div>
      <div class="shelters" v-if="shelters.length">
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
            <h2>
              {{ shelter.name }}
              <el-button v-if="isShelterOwner(shelter)"  @click.stop="editShelter(shelter.id)">
                <el-icon>
                  <Edit />
                </el-icon>
              </el-button>
              <el-button v-if="isShelterOwner(shelter)" @click.stop="deleteShelter(shelter.id)">
                <el-icon>
                  <Delete />
                </el-icon>
              </el-button>
            </h2>

            <div v-if="isShelterOwner(shelter)" style="color: gray; font-size: 0.8rem">Ваш приют</div>

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

              <div style="font-size: 14px; margin-bottom: 0" title="Популярность среди пользователей">Пользовательский рейтинг: {{ shelter.rating }}</div>
              <div style="font-size: 14px" title="Среднее время на передачу животное в добрые руки">Рейтинг эффективности (дни): {{ shelter.efficiency_rating }}</div>
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
      <div v-else class="shelters">
        Приюты не найдены. Попробуйте изменить критерии поиска.
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";
import {ElNotification} from "element-plus";
import { Delete, Edit } from '@element-plus/icons-vue'

export default {
  name: "ShelterList",
  components: {
    Delete,
    Edit
  },
  data() {
    return {
      shelters: [],
      searchText: this.$route.query.q || '',
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
      cities: [],
      selectedCity: '',
      selectedRating: [0,5],

      isAuthenticated: false,
      user: null,

      debouncedGetShelters: _.debounce(this.getShelters, 300),
    };
  },
  methods: {
    async getUserDetails() {
      try {
        const response = await axios.get("/api/v1/user-details/");
        this.user = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.getUserDetails();
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при получении данных пользователя',
            type: 'error',
          });
        }
      }
    },
    isShelterOwner(shelter) {
      return this.user && shelter.owner === this.user.id;
    },
    editShelter(id) {
      this.$router.push(`/shelters/${id}/edit`);
    },
    async deleteShelter(id) {
      try {
        await this.$confirm('Вы действительно хотите удалить приют?', 'Внимание', {
          confirmButtonText: 'Да',
          cancelButtonText: 'Нет',
          type: 'warning'
        });
        await axios.delete(`/api/v1/shelters/${id}/`);
        await this.getShelters();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.deleteShelter(id);
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при удалении приюта',
            type: 'error',
          });
        }
      }
    },
    async getShelters() {
      try {
        const response = await axios.get("/api/v1/shelters/", {
          params: {
            page: this.currentPage,
            per_page: this.perPage,
            search: this.searchText,
            city: this.selectedCity,
            rating_min: this.selectedRating[0],
            rating_max: this.selectedRating[1],
          }
        });

        this.shelters = response.data.results;
        this.totalPages = response.data.total_pages;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.getShelters();
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при получении списка приютов',
            type: 'error',
          });
        }
      }
    },
    async getCities() {
      try {
        const response = await axios.get("/api/v1/shelters/cities/");
        this.cities = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.getCities();
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при получении списка городов для фильтра',
            type: 'error',
          });
        }
      }
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
    addShelter(){
      this.$router.push(`/shelters/add`);
    }
  },
  watch: {
    perPage: {
      handler() {
        this.changePerPage();
      },
      immediate: true
    },
    '$route': function() {
      this.isAuthenticated = !!localStorage.getItem('access');
    }
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem('access');
    if (this.isAuthenticated){
      this.getUserDetails();
    }
    this.getShelters();
    this.getCities();
  }
};
</script>

<style scoped>
.shelter-manage-buttons {
  position: absolute;
  right: 0;
  top: 10px;
}

.shelter-search{
  padding: 1rem 0;
}

.shelter-list {
  width: 80%;
  margin: 0 auto;
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

.filter-label{
  /*margin-bottom: 1rem;*/
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
  margin-bottom: 0.5rem;
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