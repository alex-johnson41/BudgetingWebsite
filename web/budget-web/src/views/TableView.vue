<template>
    <v-select v-model="selectedYear" :items="years" @update:modelValue="getData()" width="15%">
    </v-select>
    <table width="90%" class="ml-10 mt-5">
        <thead>
            <tr>
                <th width="15%">Categories</th>
                <th v-for="month in horizontalHeaders" :key="month" width="6.5%">{{ month }}</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: green">
                <td>INCOME</td>
                <td v-for="month in horizontalHeaders" :key="month"></td>
                <td></td>
            </tr>
            <tr v-for="category in incomeHeaders" :key="category.id">
                <td>{{ category.name }}</td>
                <td v-for="month in horizontalHeaders" :key="month">
                    {{ calculateCellTotal(category.id, monthToNum(month)) }}
                </td>
                <td>{{ calculateCategoryTotal(category.id) }}</td>
            </tr>
            <tr style="background-color: red">
                <td>EXPENSES</td>
                <td v-for="month in horizontalHeaders" :key="month"></td>
                <td></td>
            </tr>
            <tr v-for="category in expenseHeaders" :key="category.id">
                <td>{{ category.name }}</td>
                <td v-for="month in horizontalHeaders" :key="month">
                    {{ calculateCellTotal(category.id, monthToNum(month)) }}
                </td>
                <td>{{ calculateCategoryTotal(category.id) }}</td>
            </tr>
            <tr style="background-color: blue">
                <td>TOTALS</td>
                <td v-for="month in horizontalHeaders" :key="month"></td>
                <td></td>
            </tr>
            <tr>
                <td>Income:</td>
                <td v-for="month in horizontalHeaders" :key="month">
                    {{ calculateMonthTotal(monthToNum(month), true) }}
                </td>
                <td>{{ calculateTotal(true) }}</td>
            </tr>
            <tr>
                <td>Expenses:</td>
                <td v-for="month in horizontalHeaders" :key="month">
                    {{ calculateMonthTotal(monthToNum(month), false) }}
                </td>
                <td>{{ calculateTotal(false) }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import _ from "underscore";

export default {
    components: {},
    data: () => ({
        transactions: [],
        verticalHeaders: [],
        horizontalHeaders: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
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
            this.transactions = await this.$api.get(
                `transaction/1/filter?year=${this.selectedYear}`
            ); //TODO: HARD CODED USER ID AND YEAR
            var categories = await this.$api.get("category/user/1"); //TODO: HARD CODED USER ID
            this.incomeHeaders = _.where(categories, { is_income: true });
            this.expenseHeaders = _.where(categories, { is_income: false });
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
            return total == 0 ? "" : "$" + total.toFixed(2);
        },
        calculateCategoryTotal(categoryId) {
            var total = 0;
            var filteredTransactions = _.where(this.transactions, { category_id: categoryId });
            filteredTransactions.forEach((transaction) => {
                total += transaction.amount;
            });
            return total == 0 ? "" : "$" + total.toFixed(2);
        },
        calculateMonthTotal(month, is_income) {
            var total = 0;
            this.transactions.forEach((transaction) => {
                const transactionMonth = new Date(transaction.date + "T00:00:00").getMonth();
                if (transactionMonth === month && transaction.category.is_income == is_income) {
                    total += transaction.amount;
                }
            });
            return total == 0 ? "" : "$" + total.toFixed(2);
        },
        calculateTotal(is_income) {
            var total = 0;
            this.transactions.forEach((transaction) => {
                if (transaction.category.is_income == is_income) {
                    total += transaction.amount;
                }
            });
            return total == 0 ? "" : "$" + total.toFixed(2);
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
