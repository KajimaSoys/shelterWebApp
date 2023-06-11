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
    fetchAnimal() {
      axios.get(`api/v1/animals/${this.$route.params['animalId']}/`)
        .then(response => {
          this.animal = response.data;
        })
        .catch(error => {
          console.error(error);
        })
    }
  }
};
</script>

<style scoped>

</style>

