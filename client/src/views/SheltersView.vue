<template>
  <div>
    <Navbar />
    <ShelterList />
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import ShelterList from "@/components/shelter/ShelterList.vue";

export default {
  name: "SheltersView",
  components: {
    Navbar,
    Footer,
    ShelterList
  }
};
</script>

<style scoped>

</style>