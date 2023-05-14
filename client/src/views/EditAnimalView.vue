<template>
  <div>
    <Navbar />
    <div class="form-container">
      <EditAnimalForm />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import EditAnimalForm from "@/components/animal/EditAnimalForm.vue";

export default {
  name: "EditAnimalView",
  components: {
    Navbar,
    Footer,
    EditAnimalForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>


