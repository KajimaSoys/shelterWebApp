<template>
  <div>
    <Navbar />
    <div class="form-container">
      <EditFundraisingForm />
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import EditFundraisingForm from "@/components/fundraising/EditFundraisingForm.vue";

export default {
  name: "EditFundraisingView",
  components: {
    Navbar,
    Footer,
    EditFundraisingForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>