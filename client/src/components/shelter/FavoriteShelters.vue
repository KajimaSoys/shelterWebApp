<template>
  <div class="favorite-shelters">
    <el-card v-for="shelter in shelters.slice(0,4)" :key="shelter.id" @click="goToShelter(shelter.id)" class="shelter-card">
<!--      <div class="shelter-card-image">-->
<!--        <img v-if="shelter.photos.length > 0" :src="shelter.photos[0].photo">-->
<!--        <img v-else src="/no-photo.gif">-->
<!--      </div>-->
      <div class="shelter-card-content">
        <h2>
          {{ shelter.name }}
        </h2>
        <div class="shelter-card-info">
          <div><b>Адрес:</b> {{ shelter.city }}, {{ shelter.street }}{{ shelter.house !== '' ? `, ${shelter.house}`: ''}}</div>

          <div><b>Телефон: </b>
            <a :href="`tel:${shelter.phone_number}`" @click.stop>
              {{ shelter.phone_number }}
            </a>
          </div>
          <div><b>Email:</b> {{ shelter.email }}</div>
          <div style="font-size: 14px; margin-bottom: 0" title="Популярность среди пользователей">Пользовательский рейтинг: {{ shelter.rating }}</div>
          <div style="font-size: 14px" title="Среднее время на передачу животное в добрые руки">Рейтинг эффективности (дни): {{ shelter.efficiency_rating }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import {ElNotification} from "element-plus";

export default {
  name: "FavoriteShelters",
  data(){
    return{
      shelters: [],
    }
  },
  created() {
    this.getShelters()
  },
  methods: {
    async getShelters() {
      try {
        const response = await axios.get("/api/v1/shelters/");
        this.shelters = response.data.results;
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
    goToShelter(id) {
      this.$router.push(`/shelter/${id}`);
    },
  }
}
</script>

<style scoped>
.favorite-shelters{
  width: 90%;
  margin: auto;
  display: flex;
  flex-direction: row;
  gap: 2rem;
  position: relative;
  z-index: 4;
}

.shelter-card{
  flex: 1;
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

.shelter-card-content{
  width: 100%;
  flex-basis: 100%;
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
  text-align: left;
}

.shelter-card-info a{
  color: var(--el-color-primary);
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.shelter-card-info a:hover{
  color: var(--el-color-primary-dark-1);
}
html.dark .el-card {
  --el-card-bg-color: none;
  backdrop-filter: blur(4px) brightness(0.4);
}
</style>