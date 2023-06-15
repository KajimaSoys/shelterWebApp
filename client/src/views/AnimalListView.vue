<template>
  <Navbar />
  <AnimalMainList
      v-if="animals != null"
      :animals="animals"
      :user="user"
      @reFetchAnimals="fetchAnimals"
  />
  <Footer />
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import AnimalMainList from "@/components/animal/AnimalMainList.vue";
import axios from "axios";
import {ElNotification} from "element-plus";

export default {
  name: "AnimalListView",
  components: {
    Navbar,
    Footer,
    AnimalMainList,
  },
  data(){
    return{
      animals: null,
      user: null,
    }
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem('access');
    if (this.isAuthenticated){
      this.getUserDetails();
    }
    this.fetchAnimals();
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
    async fetchAnimals() {
      try {
        const response = await axios.get(`api/v1/animals/`);
        this.animals = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.fetchAnimals();
        } else {
          console.error(error);
        }
      }
    },
  }
}
</script>

<style scoped>

</style>