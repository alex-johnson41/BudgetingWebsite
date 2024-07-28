<template>
    <v-row class="ml-10 mt-5 mb-0" width="100%">
        <div class="d-flex align-end" style="width: 20%">
            <p class="mr-2"><b>Select Year:</b></p>
            <v-select
                variant="underlined"
                v-model="selectedYear"
                :items="years"
                @update:modelValue="getData()"
                class="pa-0 ma-0"
                density="compact"
                solo
                hide-details
            >
            </v-select>
        </div>
    </v-row>
    <v-row class="mx-10 mb-10 mt-0">
        <table width="100%">
            <thead>
                <tr>
                    <th width="15%">Categories</th>
                    <th v-for="month in horizontalHeaders" :key="month" width="6.5%">
                        {{ month }}
                    </th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: lightgreen">
                    <td>INCOME</td>
                    <td v-for="month in horizontalHeaders" :key="month"></td>
                    <td></td>
                </tr>
                <tr v-for="category in incomeHeaders" :key="category.id">
                    <td>{{ category.name }}</td>
                    <td v-for="month in horizontalHeaders" :key="month" style="text-align: right">
                        {{ displayValue(calculateCellTotal(category.id, monthToNum(month))) }}
                    </td>
                    <td style="text-align: right">
                        {{ displayValue(calculateCategoryTotal(category.id)) }}
                    </td>
                </tr>
                <tr style="background-color: lightcoral">
                    <td>EXPENSES</td>
                    <td v-for="month in horizontalHeaders" :key="month"></td>
                    <td></td>
                </tr>
                <tr v-for="category in expenseHeaders" :key="category.id">
                    <td>{{ category.name }}</td>
                    <td v-for="month in horizontalHeaders" :key="month" style="text-align: right">
                        {{ displayValue(calculateCellTotal(category.id, monthToNum(month))) }}
                    </td>
                    <td style="text-align: right">
                        {{ displayValue(calculateCategoryTotal(category.id)) }}
                    </td>
                </tr>
                <tr style="background-color: lightblue">
                    <td>TOTALS</td>
                    <td v-for="month in horizontalHeaders" :key="month"></td>
                    <td></td>
                </tr>
                <tr>
                    <td>Income:</td>
                    <td v-for="month in horizontalHeaders" :key="month" style="text-align: right">
                        {{ displayValue(calculateMonthTotal(monthToNum(month), true)) }}
                    </td>
                    <td style="text-align: right">{{ displayValue(calculateTotal(true)) }}</td>
                </tr>
                <tr>
                    <td>Expenses:</td>
                    <td v-for="month in horizontalHeaders" :key="month" style="text-align: right">
                        {{ displayValue(calculateMonthTotal(monthToNum(month), false)) }}
                    </td>
                    <td style="text-align: right">{{ displayValue(calculateTotal(false)) }}</td>
                </tr>
                <tr>
                    <td>Net:</td>
                    <td v-for="month in horizontalHeaders" :key="month" style="text-align: right">
                        {{
                            displayValue(
                                calculateMonthTotal(monthToNum(month), true) - calculateMonthTotal(monthToNum(month), false)
                            )
                        }}
                    </td>
                    <td style="text-align: right">
                        {{ displayValue(calculateTotal(true) - calculateTotal(false)) }}
                    </td>
                </tr>
            </tbody>
        </table>
    </v-row>
</template>

<script>
import _ from "underscore";
import { numberWithCommas } from "@/utilities.js";

export default {
    components: {},
    data: () => ({
        transactions: [],
        verticalHeaders: [],
        horizontalHeaders: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        incomeHeaders: [],
        expenseHeaders: [],
        years: [],
        selectedYear: new Date().getFullYear().toString(),
    }),
    computed: {},
    async mounted() {
        this.transactions = await this.$api.get(`transaction/user/1`); //TODO: HARD CODED USER ID AND YEAR
        this.years = this.transactions
            .map((transaction) => new Date(transaction.date + "T00:00:00").getFullYear())
            .filter((value, index, self) => self.indexOf(value) === index);
        this.getData();
    },
    methods: {
        async getData() {
            this.transactions = await this.$api.get(`transaction/1/filter?year=${this.selectedYear}`); //TODO: HARD CODED USER ID AND YEAR
            var categories = await this.$api.get("category/user/1"); //TODO: HARD CODED USER ID
            this.incomeHeaders = _.where(categories, { is_income: true });
            this.expenseHeaders = _.where(categories, { is_income: false });
        },
        displayValue(value) {
            return value == 0
                ? ""
                : value < 0
                ? "-$" + numberWithCommas((value * -1).toFixed(2))
                : "$" + numberWithCommas(value.toFixed(2));
        },
        calculateCellTotal(categoryId, month) {
            var filteredTransactions = _.where(this.transactions, { category_id: categoryId });
            var total = 0;
            filteredTransactions.forEach((transaction) => {
                const transactionMonth = new Date(transaction.date + "T00:00:00").getMonth();
                if (transactionMonth === month) {
                    total += transaction.amount;
                }
            });
            return total;
        },
        calculateCategoryTotal(categoryId) {
            var total = 0;
            var filteredTransactions = _.where(this.transactions, { category_id: categoryId });
            filteredTransactions.forEach((transaction) => {
                total += transaction.amount;
            });
            return total;
        },
        calculateMonthTotal(month, is_income) {
            var total = 0;
            this.transactions.forEach((transaction) => {
                const transactionMonth = new Date(transaction.date + "T00:00:00").getMonth();
                if (transactionMonth === month && transaction.category.is_income == is_income) {
                    total += transaction.amount;
                }
            });
            return total;
        },
        calculateTotal(is_income) {
            var total = 0;
            this.transactions.forEach((transaction) => {
                if (transaction.category.is_income == is_income) {
                    total += transaction.amount;
                }
            });
            return total;
        },
        monthToNum(month) {
            switch (month) {
                case "Jan":
                    return 0;
                case "Feb":
                    return 1;
                case "Mar":
                    return 2;
                case "Apr":
                    return 3;
                case "May":
                    return 4;
                case "Jun":
                    return 5;
                case "Jul":
                    return 6;
                case "Aug":
                    return 7;
                case "Sep":
                    return 8;
                case "Oct":
                    return 9;
                case "Nov":
                    return 10;
                case "Dec":
                    return 11;
                default:
                    return -1;
            }
        },
    },
};
</script>
<style scoped>
table,
th,
td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
