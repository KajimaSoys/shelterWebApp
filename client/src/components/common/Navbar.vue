<template>

  <el-button @click="logout">Logout</el-button>

</template>

<script>
export default {
  name: "Navbar",
   methods: {
    logout() {

      localStorage.removeItem("authToken");


      this.$router.push("/login");
    }
  }
}
</script>

<style scoped>

</style>