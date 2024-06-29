<template>
  <v-app-bar :elevation="2">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-app-bar-title>Budgeting Website</v-app-bar-title>
      <v-btn-toggle class="ml-10" rounded="4" group variant="outlined">
        <v-btn value="left"> Dashboard </v-btn>
        <v-btn value="center"> YTD </v-btn>
        <v-btn value="right"> Add Data </v-btn>
        <v-btn value="justify"> Settings </v-btn>
      </v-btn-toggle>
    </template>

    <template v-slot:append>
      <v-btn icon="mdi-dots-vertical"></v-btn>
    </template>
  </v-app-bar>
</template>
<script>
export default {
  name: "TopBar",
  data: () => ({
    //
  }),
};
</script>
