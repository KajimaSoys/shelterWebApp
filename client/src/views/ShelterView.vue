<template>
    <Navbar />
    <ShelterInfo v-if="shelter != null" :shelter="shelter" />
    <AnimalList v-if="shelter != null" :animals="shelter.animals" />
    <FundsSpent v-if="shelter != null" :moneyReports="shelter.money_reports" />
    <Footer />
</template>

<script>
import axios from 'axios';
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import ShelterInfo from "@/components/shelter/ShelterInfo.vue";
import AnimalList from "@/components/animal/AnimalList.vue";
import FundsSpent from "@/components/shelter/FundsSpent.vue";

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
      shelter: null
    }
  },
  created() {
    this.fetchShelter();
  },
  methods: {
    fetchShelter() {
      axios.get(`api/v1/shelters/${this.$route.params.id}/`)
        .then(response => {
          this.shelter = response.data;
        })
        .catch(error => {
          console.error(error);
        })
    }
  }
};
</script>