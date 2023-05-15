<template>
  <div class="main-background"> </div>
  <Navbar />
  <Search />
  <FavoriteShelters />
  <SearchResult />
  <Footer />
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

.main-background{
  /*background:;*/
  width: 100%;
  height: 100%;
  position: absolute;
  background-image: linear-gradient(rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.2) 48.37%, rgba(0, 0, 0, 0.3) 100%),  url("/main-background.jpg");
  background-size: cover;
  background-position: center center;
  transform: scale(1);
}

</style>