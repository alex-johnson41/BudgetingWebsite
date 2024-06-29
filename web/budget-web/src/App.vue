<template>
  <v-app>
    <top-bar />
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import TopBar from "./components/TopBar.vue";
export default {
  name: "App",

  components: {
    HelloWorld,
    TopBar,
  },

  data: () => ({
    //
  }),
};
</script>
