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
        <div v-if="display === 'budget'"><budget-editor /></div>
        <div v-if="display === 'category'"><category-editor /></div>
        <div v-if="display === 'settings'">settings</div>
    </v-container>
</template>

<script>
import CategoryEditor from "@/components/setup/CategoryEditor.vue";
import BudgetEditor from "@/components/setup/BudgetEditor.vue";

export default {
    name: "SetupView",
    components: {
        CategoryEditor,
        BudgetEditor,
    },
    data: () => ({
        display: "budget",
    }),
    methods: {},
};
</script>
