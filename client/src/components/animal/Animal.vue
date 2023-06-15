<template>
  <div class="animal">
    <h1>
      {{ animal.name }}
      <el-button v-if="isShelterOwner"  @click.stop="editAnimal(animal.shelter, animal.id)">
        <el-icon>
          <Edit />
        </el-icon>
      </el-button>
      <el-button v-if="isShelterOwner" @click.stop="deleteAnimal(animal.shelter, animal.id)">
        <el-icon>
          <Delete />
        </el-icon>
      </el-button>
    </h1>
    <div class="animal-content">
      <div class="animal-content-images">
        <swiper
          v-if="animal.photos.length > 0"
          :modules="modules"
          :slides-per-view="slidesPerView"
          :space-between="16"
          :navigation="navigation"
          :pagination="pagination"
        >
          <swiper-slide
            v-for="(photo, index) in animal.photos"
            :key="index"
            class="image-card"
          >
            <a :href="photo.photo" target="_blank"><img :src="photo.photo" :key="photo.id" alt="Изображение приюта"></a>
          </swiper-slide>
        </swiper>

        <img v-else src="/no-photo.gif">

        <div class="swiper-controls" v-if="animal.photos.length > 1">
          <div class="swiper-button-prev swiper-button-prev-1">
            <svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M8.0973 0.156443L0.183064 8.53296L0.182131 8.53401L0.172611 8.54412C-0.0572777 8.78808 -0.0578003 9.2114 0.172625 9.456L0.181719 9.46565L0.182583 9.46662L8.09723 17.8436C8.29484 18.0527 8.58788 18.0522 8.78497 17.8416C9.01494 17.5958 9.01372 17.1747 8.78313 16.9306L1.86931 9.61291H19.4835C19.7116 9.61291 20 9.39746 20 9.00001C20 8.60256 19.7116 8.3871 19.4835 8.3871H1.86919L8.78325 1.06935C9.01382 0.825229 9.01501 0.404166 8.78505 0.158436C8.58785 -0.0522866 8.29489 -0.0526697 8.0973 0.156443Z" fill="black"/>
            </svg>
          </div>
          <div class="swiper-pagination swiper-pagination-1"></div>
          <div class="swiper-button-next swiper-button-next-1">
            <svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M11.9027 0.156443L19.8169 8.53296L19.8179 8.53401L19.8274 8.54412C20.0573 8.78808 20.0578 9.2114 19.8274 9.456L19.8183 9.46565L19.8174 9.46662L11.9028 17.8436C11.7052 18.0527 11.4121 18.0522 11.215 17.8416C10.9851 17.5958 10.9863 17.1747 11.2169 16.9306L18.1307 9.61291H0.516543C0.288381 9.61291 0 9.39746 0 9.00001C0 8.60256 0.288382 8.3871 0.516543 8.3871H18.1308L11.2168 1.06935C10.9862 0.825229 10.985 0.404166 11.215 0.158436C11.4121 -0.0522866 11.7051 -0.0526697 11.9027 0.156443Z" fill="black"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="animal-content-info">
        <div v-html="animal.description"> </div>

        <div>Тип животного:e: {{ animal.animal_type }}</div>

        <div>Порода: {{ animal.breed }}</div>

        <div>Возраст (месяцы): {{ animal.age }}</div>

        <div>Пол: {{ genderChoices[animal.gender] }}</div>

        <div>Вес (граммы): {{ animal.weight }}</div>

        <div>Состояние здоровья: {{ animal.health_status }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { Navigation, Pagination, Scrollbar, A11y } from 'swiper';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import {Delete, Edit} from "@element-plus/icons-vue";
import axios from "axios";
import {ElNotification} from "element-plus";

export default {
  name: "Animal",
  props: {
    animal: {
      type: Object,
      required: true
    }
  },
  components: {
    Swiper,
    SwiperSlide,
    Delete,
    Edit
  },
  data () {
    return{
      genderChoices: {
        'male': 'Самец',
        'female': 'Самка',
        'unknown': 'Неизвестно',
      },
      user:null,

      modules: [Navigation, Pagination, A11y],
      slidesPerView: 1,
      navigation: { nextEl: '.swiper-button-next-1', prevEl: '.swiper-button-prev-1' },
      pagination: { el: '.swiper-pagination-1', clickable: true, bulletClass: 'swiper-pagination-bullet', bulletActiveClass: 'swiper-pagination-bullet-active' },
    }
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem('access');
    if (this.isAuthenticated){
      this.getUserDetails();
    }
  },
  computed: {
    isShelterOwner() {
      return this.user && this.animal.shelter_owner === this.user.id;
    },
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
    editAnimal(id, animalId) {
      this.$router.push(`/shelter/${id}/animal/${animalId}/edit`);
    },
    async deleteAnimal(id, animalId) {
      try {
        await this.$confirm('Вы действительно хотите удалить животное?', 'Внимание', {
          confirmButtonText: 'Да',
          cancelButtonText: 'Нет',
          type: 'warning'
        });
        await axios.delete(`/api/v1/animals/${animalId}/`);
        this.$router.push(`/shelter/${id}`)
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.deleteShelter(id);
        } else {
          console.error(error);
          ElNotification({
            title: 'Ошибка!',
            message: 'Произошла ошибка при удалении животного',
            type: 'error',
          });
        }
      }
    },
  }
};
</script>

<style scoped>
animal {
  /*width: 80%;*/
}

.animal-content {
  display: flex;
  flex-direction: row;
  width: 80%;
  margin: 0 auto;
  gap: 3rem;
}

.animal-content-images{
  width: 35%;
  flex-basis: 35%;
}

.image-card img{
  width: 100%;
  object-fit: cover;
}

/*img {*/
/*  width: 100px;*/
/*  height: 100px;*/
/*}*/

.swiper-controls {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 50px;
  flex-direction: row;
  gap: 30px;
}


.swiper-button-next,
.swiper-button-prev {
  border-radius: 50%;
  border: 1px solid #BDBDBD;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: inherit;
}

.swiper-button-prev svg, .swiper-button-next svg{
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Chrome, Safari, Opera */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Нестандартное свойство */
}

svg path{
  transition: fill 0.2s ease-in-out;
}

.swiper-button-next svg path, .swiper-button-prev svg path{
  fill: #ffffff;
}

.swiper-button-next:hover svg path, .swiper-button-prev:hover svg path{
  fill: #ff5555;
}

.swiper-button-next:after, .swiper-button-prev:after {
  content: none;
}
.swiper-button-next:after, .swiper-button-prev:after {
  font-family: none;
  font-size: none;
  text-transform: none!important;
  letter-spacing: 0;
  font-variant: initial;
  line-height: 1;
}

.swiper-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  position: inherit;
}

.swiper-pagination-bullets.swiper-pagination-horizontal{
  width: inherit;
}

:deep(.swiper-pagination-bullet) {
  background: #ffffff;
}

:deep(.swiper-pagination-bullet.swiper-pagination-bullet-active) {
  background: #ff5555;
}

:deep(.swiper-wrapper) {
  align-items: center;
  height: 350px;
}

:deep(.swiper-slide) {
  display: flex;
}

:deep(.swiper-slide a) {
  display: flex;
  width: 100%;
}

.animal-content-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.7rem;
}

.animal-content-info a{
  color: var(--el-color-primary);
  text-decoration: none;
  transition: all 0.3s ease-in-out;
}

.animal-content-info a:hover{
  color: var(--el-color-primary-dark-1);
}
</style>
