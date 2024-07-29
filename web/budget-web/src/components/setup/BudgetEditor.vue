<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-card elevation="0" class="ma-0 pa-0">
        <v-card-title style="font-size: 30px">Create Your Budget</v-card-title>
        <v-card-text>
            <v-row>
                <v-col cols="3">
                    <v-select
                        v-model="selectedMonth"
                        :items="months"
                        label="Select Month"
                        density="compact"
                        item-title="text"
                        @update:modelValue="refreshTable"
                    ></v-select>
                    <v-select
                        v-model="selectedYear"
                        :items="years"
                        label="Select Year"
                        density="compact"
                        @update:modelValue="refreshTable"
                    ></v-select>
                </v-col>
                <v-col cols="3">
                    <p class="remaining-amount">Remaining Amount: ${{ totalRemainingAmount }}</p>
                    <v-btn variant="outlined" color="green" @click="importBudget">Import From Last Month</v-btn>
                    <v-btn class="save-cancel-btns" variant="outlined" color="red" @click="refreshTable">Cancel</v-btn>
                    <v-btn class="save-cancel-btns" variant="outlined" color="primary" @click="save">Save</v-btn>
                </v-col>
            </v-row>
            <v-row justify="center" class="mt-0 pt-0">
                <v-col cols="6">
                    <v-data-table-virtual
                        class="data-table"
                        density="compact"
                        :headers="headers"
                        :items="incomeBudgets"
                        :sort-by="[{ key: 'category.name', order: 'asc' }]"
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
                <v-col cols="6">
                    <v-data-table-virtual
                        class="data-table"
                        density="compact"
                        :headers="headers"
                        :items="expenseBudgets"
                        :sort-by="[{ key: 'category.name', order: 'asc' }]"
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
        </v-card-text>
    </v-card>
</template>
<script>
import _ from "underscore";
import * as cloneDeep from "lodash.clonedeep";
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
                this.originalBudgets = response;
            }); // TODO: HARD CODED USER ID
            await this.$api.get("category/user/1").then((response) => {
                this.categories = response;
            }); // TODO: HARD CODED USER ID
            this.initializeBudget();
        },
        initializeBudget() {
            this.budgets = cloneDeep(this.originalBudgets);
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
        async importBudget() {
            await this.$api
                .get(`budget/user/1/filter?year=${this.selectedYear}&month=${this.selectedMonth - 1}`)
                .then((response) => {
                    if (response.length > 0) {
                        this.budgets = response;
                    } else {
                        this.originalBudgets = [];
                        this.initializeBudget();
                    }
                });
        },
        save() {
            console.log(this.budgets);
            console.log(this.originalBudgets);
            const promises = this.budgets.forEach(async (budget) => {
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
                    const originalBudget = this.originalBudgets.find((b) => b.id === budget.id);
                    if (_.isEqual(originalBudget, budget) == false) {
                        const updatedBudget = {
                            amount: budget.amount,
                        };
                        await this.$api.patch(`budget/${budget.id}`, updatedBudget);
                    }
                }
            });
            Promise.all(promises).then(async () => {
                await this.refreshTable();
            });
        },
        async cancel() {
            await this.refreshTable();
        },
    },
};
</script>
<style scoped>
.remaining-amount {
    position: relative;
    top: -5px;
    font-size: 20px;
    font-weight: 500;
}
.v-btn {
    height: 33px;
    margin-right: 5px;
}
.save-cancel-btns {
    margin-top: 10px;
}
.data-table {
    max-height: 400px;
}
</style>
