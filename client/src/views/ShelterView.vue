<template>
    <Navbar />
    <ShelterInfo
        v-if="shelter != null"
        :shelter="shelter"
        :owner="isShelterOwner"
    />
    <AnimalList
        v-if="shelter != null"
        :animals="shelter.animals"
        :owner="isShelterOwner"
        @reFetchShelter="fetchShelter"
    />
    <FundsSpent
        v-if="shelter != null"
        :moneyReports="shelter.money_reports"
        :owner="isShelterOwner"
        @reFetchShelter="fetchShelter"
    />
    <Footer />
</template>

<script>
import axios from 'axios';
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import ShelterInfo from "@/components/shelter/ShelterInfo.vue";
import AnimalList from "@/components/animal/AnimalList.vue";
import FundsSpent from "@/components/shelter/FundsSpent.vue";
import {ElNotification} from "element-plus";

export default {
  name: "ShelterView",
  components: {
    Navbar,
    Footer,
    ShelterInfo,
    AnimalList,
    FundsSpent
  },
  props: [
    'id',
  ],
  data() {
    return {
      shelter: null,
      user: null,
    }
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem('access');
    if (this.isAuthenticated){
      this.getUserDetails();
    }
    this.fetchShelter();
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
    async fetchShelter() {
      try {
        const response = await axios.get(`api/v1/shelters/${this.$route.params.id}/`);
        this.shelter = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.fetchShelter();
        } else {
          console.error(error);
        }
      }
    },
  },
  computed: {
    isShelterOwner() {
      return this.user && this.shelter.owner === this.user.id;
    },
  }
};
</script>