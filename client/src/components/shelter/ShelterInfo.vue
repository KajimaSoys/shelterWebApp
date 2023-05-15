<template>
    <div>
        <h1>{{ shelter.name }}</h1>
        <img v-for="photo in shelter.photos" :src="photo.photo" :key="photo.id" alt="Shelter photo">
        <p><strong>Описание: </strong>{{ shelter.description }}</p>
        <p><strong>Город: </strong>{{ shelter.city }}</p>
        <p><strong>Улица: </strong>{{ shelter.street }}</p>
        <p><strong>Дом: </strong>{{ shelter.house }}</p>
        <p><strong>Телефон: </strong>{{ shelter.phone_number }}</p>
        <p><strong>Email: </strong>{{ shelter.email }}</p>
        <p><strong>Сайт: </strong><a :href="shelter.website_link">{{ shelter.website_link }}</a></p>
        <p><strong>Instagram: </strong><a :href="shelter.instagram_link">{{ shelter.instagram_link }}</a></p>
        <p><strong>Telegram: </strong><a :href="shelter.telegram_link">{{ shelter.telegram_link }}</a></p>
        <p><strong>VK: </strong><a :href="shelter.vk_link">{{ shelter.vk_link }}</a></p>
    </div>
</template>

<script>
export default {
  name: "ShelterInfo",
  props: {
    shelter: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
img {
  width: 100px;
  height: 100px;
}
</style>