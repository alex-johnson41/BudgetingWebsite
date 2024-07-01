<template>
    <v-app>
        <v-app-bar :elevation="2">
            <template v-slot:prepend>
                <v-app-bar-nav-icon></v-app-bar-nav-icon>
                <v-app-bar-title>Budgeting Website</v-app-bar-title>
                <v-btn-toggle class="ml-10" rounded="4" group variant="outlined">
                    <v-btn to="/dashboard" value="left"> Dashboard </v-btn>
                    <v-btn to="/table" value="center"> Table </v-btn>
                    <v-btn to="/data" value="right"> Transactions </v-btn>
                    <v-btn to="/settings" value="justify"> Settings </v-btn>
                </v-btn-toggle>
            </template>

            <template v-slot:append>
                <v-btn icon="mdi-dots-vertical"></v-btn>
            </template>
        </v-app-bar>
        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script>
import { RouterView } from "vue-router";
export default {
    name: "App",

    components: {
        RouterView,
    },

    data: () => ({
        //
    }),
};
</script>
