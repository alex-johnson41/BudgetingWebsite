<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-row class="pt-0 mt-5" justify="center">
        <v-col cols="5">
            <v-row>
                <v-col cols="6">
                    <v-select
                        v-model="selectedMonth"
                        :items="months"
                        label="Select Month"
                        dense
                        item-title="text"
                        @update:modelValue="refreshTable"
                    ></v-select>
                </v-col>
                <v-col cols="6">
                    <v-select
                        v-model="selectedYear"
                        :items="years"
                        label="Select Year"
                        dense
                        @update:modelValue="refreshTable"
                    ></v-select>
                </v-col>
            </v-row>
        </v-col>
        <v-col cols="5">
            <v-card>
                <v-card-title>Total Remaining Amount</v-card-title>
                <v-card-text>
                    {{ totalRemainingAmount }}
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="save">Save</v-btn>
                    <v-btn color="secondary" @click="refreshTable">Cancel</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
    <v-row class="pt-0 mt-5" justify="center">
        <v-col cols="5">
            <v-data-table-virtual
                density="compact"
                :headers="headers"
                :items="incomeBudgets"
                :sort-by="[{ key: 'name', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar>
                        <v-toolbar-title>Income</v-toolbar-title>
                    </v-toolbar>
                </template>
                <template v-slot:[`item.amount`]="{ item }">
                    <v-text-field
                        v-model="item.amount"
                        class="mt-0"
                        density="compact"
                        single-line
                        hide-details
                        @blur="setDefault(item)"
                    ></v-text-field>
                </template>
            </v-data-table-virtual>
        </v-col>
        <v-col cols="5">
            <v-data-table-virtual
                density="compact"
                :headers="headers"
                :items="expenseBudgets"
                :sort-by="[{ key: 'name', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar>
                        <v-toolbar-title>Expenses</v-toolbar-title>
                    </v-toolbar>
                </template>
                <template v-slot:[`item.amount`]="{ item }">
                    <v-text-field
                        v-model="item.amount"
                        class="mt-0"
                        density="compact"
                        single-line
                        hide-details
                        @blur="setDefault(item)"
                    ></v-text-field>
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
        selectedMonth: new Date().getMonth() + 1,
        selectedYear: new Date().getFullYear(),
        years: [],
        months: [
            { text: "January", value: 1 },
            { text: "February", value: 2 },
            { text: "March", value: 3 },
            { text: "April", value: 4 },
            { text: "May", value: 5 },
            { text: "June", value: 6 },
            { text: "July", value: 7 },
            { text: "August", value: 8 },
            { text: "September", value: 9 },
            { text: "October", value: 10 },
            { text: "November", value: 11 },
            { text: "December", value: 12 },
        ],
    }),
    async mounted() {
        await this.refreshTable();
    },
    computed: {
        totalRemainingAmount() {
            return this.totalBudgetedIncome - this.totalBudgetedExpense;
        },
        totalBudgetedIncome() {
            return _.reduce(
                this.incomeBudgets,
                (memo, item) => {
                    return memo + parseFloat(item.amount);
                },
                0
            );
        },
        totalBudgetedExpense() {
            return _.reduce(
                this.expenseBudgets,
                (memo, item) => {
                    return memo + parseFloat(item.amount);
                },
                0
            );
        },
        incomeBudgets() {
            return _.filter(this.budgets, (item) => {
                return item.category.is_income;
            });
        },
        expenseBudgets() {
            return _.filter(this.budgets, (item) => {
                return item.category.is_income === false;
            });
        },
    },
    methods: {
        async refreshTable() {
            console.log(this.selectedMonth);
            await this.$api.get(`budget/user/1/filter?year=${this.selectedYear}&month=${this.selectedMonth}`).then((response) => {
                this.budgets = response;
            }); // TODO: HARD CODED USER ID
            await this.$api.get("category/user/1").then((response) => {
                this.categories = response;
            }); // TODO: HARD CODED USER ID
            this.initializeBudget();
        },
        initializeBudget() {
            this.categories.forEach((category) => {
                const existingBudget = this.budgets.find((budget) => budget.category_id === category.id);
                if (!existingBudget) {
                    this.budgets.push({
                        user_id: 1, // TODO: HARD CODED USER ID
                        category: category,
                        category_id: category.id,
                        amount: 0,
                        id: -1,
                        month: this.selectedMonth,
                        year: this.selectedYear,
                    });
                }
            });
        },
        setDefault(item) {
            if (item.amount == "") item.amount = 0;
        },
        save() {
            this.budgets.forEach(async (budget) => {
                if (budget.id === -1) {
                    const newBudget = {
                        user_id: budget.user_id,
                        category_id: budget.category_id,
                        amount: budget.amount,
                        month: this.selectedMonth,
                        year: this.selectedYear,
                    };
                    await this.$api.post("budget", newBudget);
                } else {
                    const updatedBudget = {
                        amount: budget.amount,
                    };
                    await this.$api.patch(`budget/${budget.id}`, updatedBudget);
                }
            });
            this.$nextTick(async () => {
                await this.refreshTable();
            });
        },
        async cancel() {
            await this.refreshTable();
        },
    },
};
</script>
<style scoped></style>
