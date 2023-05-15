<template>
    <Navbar />
    <div class="form-container">
      <AddShelterForm />
    </div>
    <Footer />
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import AddShelterForm from "@/components/shelter/AddShelterForm.vue";

export default {
  name: "AddShelterView",
  components: {
    Navbar,
    Footer,
    AddShelterForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>


