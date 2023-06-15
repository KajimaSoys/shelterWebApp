<template>
  <div class="search-container">
    <el-form class="search-form" @submit.prevent>
      <el-form-item >
        <el-input size="large" v-model="searchText" placeholder="Введите название приюта или местоположение" @keyup.enter="search()"></el-input>
      </el-form-item>
      <el-form-item class="buttons">
        <el-button type="plain" size="large" @click="goToShelters">Перейти к списку приютов</el-button>
        <el-button type="plain" size="large" @click="goToAnimals">Перейти к списку животных</el-button>
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
      this.$router.push("/animals");
    },
    search() {
      this.$router.push({ name: 'Shelters', query: { q: this.searchText } });
    }
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 6rem;
  height: 40%;
  width: 90%;
  margin-left: auto;
  margin-right: auto;
}

.search-form {
  width: 100%;
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