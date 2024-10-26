<template>
    <v-card class="half-screen-card">
        <v-card-title class="title-container">
            Overview
            <v-card-subtitle class="mt-4"> {{ currentDate }} </v-card-subtitle>
        </v-card-title>
        <v-card-text class="flex-column">
            <v-row justify="center">
                <v-col class="py-0">
                    <p class="small-text text-center">Budgeted Remaining:</p>
                    <p class="text-center" style="font-size: 30px">{{ displayValue(budgetRemaining) }}</p>
                </v-col>
                <v-col class="py-0">
                    <p class="small-text text-center">Actual Remaining:</p>
                    <p class="text-center" style="font-size: 30px">{{ displayValue(actualRemaining) }}</p>
                </v-col>
            </v-row>
            <v-row>
                <p class="ml-3 mt-3 small-text">This months transactions:</p>
            </v-row>
            <div class="data-table-container">
                <v-data-table-virtual :items="sortedTransactions" :headers="[]" density="compact" class="data-table">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td style="width: 30%" class="pl-0">{{ item.date }}</td>
                            <td style="width: 20%" class="pa-0">{{ item.category.name }}</td>
                            <td style="width: 20%" class="pa-0">
                                <v-chip density="compact" :color="item.category.is_income ? 'green' : 'red'">
                                    {{ displayValue(item.amount) }}
                                </v-chip>
                            </td>
                        </tr>
                    </template>
                </v-data-table-virtual>
            </div>
        </v-card-text>
    </v-card>
</template>

<script>
import { displayValue } from "@/utilities.js";
export default {
    props: {
        budgets: {
            type: Array,
            required: true,
        },
        transactions: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            currentDate: new Date().toLocaleDateString(),
            budgetRemaining: 0,
            actualRemaining: 0,
            sortedTransactions: [],
        };
    },
    watch: {
        transactions: {
            handler() {
                this.calculateRemainingFunds();
            },
            deep: true,
        },
    },
    mounted() {
        this.calculateRemainingFunds();
        this.sortedTransactions = [...this.transactions].sort((a, b) => {
            return new Date(b.date) - new Date(a.date);
        });
    },
    methods: {
        calculateRemainingFunds() {
            let totalBudgeted = 0;
            let totalIncome = 0;
            let totalSpent = 0;
            this.budgets.forEach((budget) => {
                if (budget.category.is_income == false) {
                    totalBudgeted += budget.amount;
                }
            });
            this.transactions.forEach((transaction) => {
                if (transaction.category.is_income == false) {
                    totalSpent += transaction.amount;
                } else {
                    totalIncome += transaction.amount;
                }
            });
            this.budgetRemaining = totalBudgeted - totalSpent;
            this.actualRemaining = totalIncome - totalSpent;
        },
        displayValue(value) {
            return displayValue(value);
        },
    },
};
</script>

<style scoped lang="scss">
@import "@/styles.scss";
.title-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-size: 30px;
}
.small-text {
    font-size: 13px;
}
.half-screen-card {
    height: 42vh;
    display: flex;
    flex-direction: column;
    background-color: $primary;
    border-radius: 20px;
}
.flex-column {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    overflow: hidden;
    padding-top: 10px;
}
.data-table {
    background-color: $secondary;
}
.data-table-container {
    background-color: $primary;
    margin-top: 15px;
    flex-grow: 1;
    overflow: auto;
}
</style>
