<template>
  <div>
    <Navbar />
    <div class="form-container">
      <AddAnimalForm />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import AddAnimalForm from "@/components/animal/AddAnimalForm.vue";

export default {
  name: "AddAnimalView",
  components: {
    Navbar,
    Footer,
    AddAnimalForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>


