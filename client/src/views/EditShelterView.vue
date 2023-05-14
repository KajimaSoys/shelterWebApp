<template>
  <div>
    <Navbar />
    <div class="form-container">
      <EditShelterForm />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import EditShelterForm from "@/components/shelter/EditShelterForm.vue";

export default {
  name: "EditShelterView",
  components: {
    Navbar,
    Footer,
    EditShelterForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>