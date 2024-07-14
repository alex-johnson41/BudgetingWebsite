<template>
    <v-container>
        <v-navigation-drawer>
            <v-list>
                <v-list-item @click="display = 'budget'" title="Budget"></v-list-item>
                <v-divider></v-divider>
                <v-list-item @click="display = 'category'" title="Category"></v-list-item>
                <v-divider></v-divider>
                <v-list-item @click="display = 'settings'" title="Settings"></v-list-item>
                <v-divider></v-divider>
            </v-list>
        </v-navigation-drawer>
        <div v-if="display === 'budget'">budget</div>
        <div v-if="display === 'category'"><CategoryEditor /></div>
        <div v-if="display === 'settings'">settings</div>
    </v-container>
</template>

<script>
import CategoryEditor from "@/components/setup/CategoryEditor.vue";

export default {
    name: "SetupView",
    components: {
        CategoryEditor,
    },
    data: () => ({
        display: "budget",
    }),
    methods: {},
};
</script>
