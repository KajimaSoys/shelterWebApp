<template>
  <div>
    <Navbar />
    <Search />
    <FavoriteShelters />
    <SearchResult />
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue';
import Footer from '@/components/common/Footer.vue';
import Search from '@/components/search/Search.vue';
import FavoriteShelters from '@/components/shelter/FavoriteShelters.vue';
import SearchResult from '@/components/search/SearchResult.vue';

export default {
  name: 'HomeView',
  components: {
    Navbar,
    Footer,
    Search,
    FavoriteShelters,
    SearchResult,
  },
};
</script>

<style scoped>

</style>