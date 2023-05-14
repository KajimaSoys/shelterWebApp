<template>
  <div>
    <Navbar />
    <Animal />
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import Animal from "@/components/animal/Animal.vue";

export default {
  name: "AnimalView",
  components: {
    Navbar,
    Footer,
    Animal
  }
};
</script>

<style scoped>

</style>

