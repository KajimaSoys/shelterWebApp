<template>
    <Navbar />
    <Animal v-if="animal != null" :animal="animal"/>
    <Footer />
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import Animal from "@/components/animal/Animal.vue";
import axios from "axios";

export default {
  name: "AnimalView",
  components: {
    Navbar,
    Footer,
    Animal
  },
  props: [
    'id',
    'animalId'
  ],
  data() {
    return {
      animal: null
    }
  },
  created() {
    this.fetchAnimal();
  },
  methods: {
    async fetchAnimal() {
      try {
        const response = await axios.get(`api/v1/animals/${this.$route.params['animalId']}/`);
        this.animal = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          await this.$refreshToken();
          return this.fetchAnimal();
        } else {
          console.error(error);
        }
      }
    },
  }
};
</script>

<style scoped>

</style>

