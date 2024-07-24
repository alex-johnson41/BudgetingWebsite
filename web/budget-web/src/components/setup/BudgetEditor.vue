<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-row class="pt-0 mt-5" justify="center">
        <v-col cols="4">
            <v-data-table-virtual
                density="compact"
                :headers="headers"
                :items="incomeBudgets"
                :sort-by="[{ key: 'name', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>Income</v-toolbar-title>
                    </v-toolbar>
                </template>
                <template v-slot:item.name="{ item }">
                    {{ item.name }}
                </template>
                <template v-slot:item.is_income="{ item }">
                    {{ item.is_income ? "Income" : "Expense" }}
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon class="me-2" size="small" @click="openEditCategoryModal(item)"> mdi-pencil </v-icon>
                    <v-icon size="small" @click="openDeleteCategoryModal(item)"> mdi-delete </v-icon>
                </template>
            </v-data-table-virtual>
        </v-col>
        <v-col cols="4">
            <v-data-table-virtual
                density="compact"
                :headers="headers"
                :items="expenseBudgets"
                :sort-by="[{ key: 'name', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>Expenses</v-toolbar-title>
                    </v-toolbar>
                </template>
                <template v-slot:item.name="{ item }">
                    {{ item.name }}
                </template>
                <template v-slot:item.is_income="{ item }">
                    {{ item.is_income ? "Income" : "Expense" }}
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon class="me-2" size="small" @click="openEditCategoryModal(item)"> mdi-pencil </v-icon>
                    <v-icon size="small" @click="openDeleteCategoryModal(item)"> mdi-delete </v-icon>
                </template>
            </v-data-table-virtual>
        </v-col>
    </v-row>
</template>
<script>
import _ from "underscore";
export default {
    components: {},
    data: () => ({
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                title: "Category",
                align: "start",
                sortable: true,
                key: "category.name",
            },
            { title: "Budgeted Amount", key: "amount" },
        ],
        categories: [],
        incomeBudgets: [],
        expenseBudgets: [],
        budgets: [],
        editedId: -1,
        editedItem: {
            name: "",
            is_income: undefined,
        },
        defaultItem: {
            name: "",
            is_income: undefined,
        },
        transactions: [],
    }),
    async mounted() {
        await this.refreshTable();
        this.initializeBudget();
    },

    methods: {
        async refreshTable() {
            await this.$api.get("budget/user/1").then((response) => {
                this.budgets = response;
                this.incomeBudgets = _.filter(response, (item) => {
                    return item.category.is_income;
                });
                this.expenseBudgets = _.filter(response, (item) => {
                    return item.category.is_income === false;
                });
            }); // TODO: HARD CODED USER ID
            await this.$api.get("category/user/1").then((response) => {
                this.categories = response;
            }); // TODO: HARD CODED USER ID
        },
        initializeBudget() {
            this.categories.forEach((category) => {
                if (this.budgets.find((budget) => budget.category.id == category.id) == undefined) {
                    this.$api.post("budget", {
                        user_id: 1,
                        category_id: category.id,
                        amount: 0,
                        month: new Date().getMonth(),
                        year: new Date().getFullYear(),
                    });
                }
            });
        },
    },
};
</script>
