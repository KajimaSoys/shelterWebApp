<template>
  <div class="search-container">
    <el-form class="search-form">
      <el-form-item >
        <el-input size="large" v-model="searchText" placeholder="Введите название приюта, местоположение или животное, которое ищете..."></el-input>
      </el-form-item>
      <el-form-item class="buttons">
        <el-button type="plain" size="large" @click="goToShelters">Перейти к списку приютов</el-button>
        <el-button type="plain" size="large" disabled @click="goToAnimals">Перейти к списку животных</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      searchText: "",
    };
  },
  methods: {
    goToShelters() {
      this.$router.push("/shelters");
    },
    goToAnimals() {
      // this.$router.push("/animals"); // TODO добавить роут
    },
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90%;
}

.search-form {
  width: 75%;
  backdrop-filter: blur(4px) brightness(0.3);
  padding: 2rem;
  border-radius: 20px;
}

.buttons {
  padding-top: 1rem;
  margin: 0;
}

:deep(.el-form-item__content) {
  justify-content: center;
}
</style>