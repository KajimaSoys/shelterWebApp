import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import AboutView from '@/views/AboutView.vue';
import SheltersView from '@/views/SheltersView.vue';
import AddShelterView from '@/views/AddShelterView.vue';
import EditShelterView from '@/views/EditShelterView.vue';
import ShelterView from '@/views/ShelterView.vue';
import AddAnimalView from '@/views/AddAnimalView.vue';
import EditAnimalView from '@/views/EditAnimalView.vue';
import AnimalView from '@/views/AnimalView.vue';
import AnimalListView from "@/views/AnimalListView.vue";
import AddFundraisingView from '@/views/AddFundraisingView.vue';
import EditFundraisingView from '@/views/EditFundraisingView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView,
    },
    {
      path: '/shelters',
      name: 'Shelters',
      component: SheltersView,
    },
    {
      path: '/animals',
      name: 'Animals',
      component: AnimalListView,
    },
    {
      path: '/shelters/add',
      name: 'AddShelter',
      component: AddShelterView,
    },
    {
      path: '/shelters/:id/edit',
      name: 'EditShelter',
      component: EditShelterView,
      props: true,
    },
    {
      path: '/shelter/:id',
      name: 'Shelter',
      component: ShelterView,
      props: true,
    },
    {
      path: '/shelter/:id/animal/add',
      name: 'AddAnimal',
      component: AddAnimalView,
      props: true,
    },
    {
      path: '/shelter/:id/animal/:animalId/edit',
      name: 'EditAnimal',
      component: EditAnimalView,
      props: true,
    },
    {
      path: '/shelter/:id/animal/:animalId',
      name: 'Animal',
      component: AnimalView,
      props: true,
    },
    {
      path: '/shelter/:id/funds/add',
      name: 'AddFunds',
      component: AddFundraisingView,
      props: true,
    },
    {
      path: '/shelter/:id/funds/:reportId/edit',
      name: 'EditFunds',
      component: EditFundraisingView,
      props: true,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
    },
  ]
})

export default router
