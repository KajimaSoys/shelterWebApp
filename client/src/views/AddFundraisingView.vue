<template>
    <Navbar />
    <div class="form-container">
      <AddFundraisingForm />
    </div>
    <Footer />
</template>

<script>
import Navbar from "@/components/common/Navbar.vue";
import Footer from "@/components/common/Footer.vue";
import AddFundraisingForm from "@/components/fundraising/AddFundraisingForm.vue";

export default {
  name: "AddFundraisingView",
  components: {
    Navbar,
    Footer,
    AddFundraisingForm,
  }
};
</script>

<style scoped>
.form-container {
  padding: 2rem;
}
</style>

