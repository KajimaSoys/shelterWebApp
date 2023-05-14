<template>
  <div>
    <Navbar />
    <ShelterInfo />
    <AnimalList />
    <FundsSpent />
    <Footer />
  </div>
</template>

<script>
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
  }
};
</script>

<style scoped>

</style>

