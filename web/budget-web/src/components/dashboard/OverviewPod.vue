<template>
    <v-card class="half-screen-card">
        <v-card-title class="title-container">
            Overview
            <v-card-subtitle class="mt-2"> {{ currentDate }} </v-card-subtitle>
        </v-card-title>
        <v-card-text class="flex-column">
            <v-row>
                <p class="ml-3 small-text">Remaining Funds:</p>
            </v-row>
            <v-row justify="center">
                <p style="font-size: 40px">${{ remainingFunds }}</p>
            </v-row>
            <v-row>
                <p class="ml-3 small-text">This months transactions:</p>
            </v-row>
            <div class="data-table-container">
                <v-data-table-virtual
                    :items="transactions"
                    :headers="[]"
                    :sort-by="[{ key: 'date', order: 'desc' }]"
                    density="compact"
                    style="background-color: lightgray"
                >
                    <template v-slot:item="{ item }">
                        <tr>
                            <td style="width: 20%" class="pl-0">{{ item.date }}</td>
                            <td style="width: 20%" class="pa-0">{{ item.category.name }}</td>
                            <td style="width: 20%" class="pa-0">${{ item.amount }}</td>
                        </tr>
                    </template>
                </v-data-table-virtual>
            </div>
        </v-card-text>
    </v-card>
</template>

<script>
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
            remainingFunds: 0,
        };
    },
    mounted() {
        this.calculateRemainingFunds();
    },
    methods: {
        calculateRemainingFunds() {
            let totalBudgeted = 0;
            let totalSpent = 0;
            console.log(this.budgets);
            this.budgets.forEach((budget) => {
                if (budget.category.is_income == false) {
                    totalBudgeted += budget.amount;
                }
            });
            this.transactions.forEach((transaction) => {
                if (transaction.category.is_income == false) {
                    totalSpent += transaction.amount;
                }
            });
            console.log(totalBudgeted);
            console.log(totalSpent);
            this.remainingFunds = (totalBudgeted - totalSpent).toFixed(2);
        },
    },
};
</script>

<style scoped>
.title-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-size: 30px;
}
.small-text {
    font-size: 15px;
}
.half-screen-card {
    height: 45vh;
    display: flex;
    flex-direction: column;
    background-color: lightgray;
    border-radius: 20px;
}
.flex-column {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    overflow: hidden;
    padding-top: 10px;
}
.data-table-container {
    margin-top: 15px;
    flex-grow: 1; /* Allow the container to grow and take up remaining space */
    overflow: auto; /* Ensure overflow is set to auto */
}
</style>
