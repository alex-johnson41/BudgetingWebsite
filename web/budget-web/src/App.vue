<template>
  <v-app>
    <side-bar />
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import SideBar from "./components/SideBar.vue";
export default {
  name: "App",

  components: {
    HelloWorld,
    SideBar,
  },

  data: () => ({
    //
  }),
};
</script>
