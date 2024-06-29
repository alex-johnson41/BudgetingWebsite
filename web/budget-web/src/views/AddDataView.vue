<template>
    <v-row class="pt-0 mt-10" justify="center">
        <v-col cols="6">
            <v-data-table :items="transactions" item-key="index">
                <template v-slot:items="props">
                    <td class="text-left">{{ props.item.date }}</td>
                    <td class="text-left">{{ "$" + props.item.amount }}</td>
                    <td class="text-left">{{ props.item.category }}</td>
                    <td class="text-left">{{ props.item.description }}</td>
                </template>
            </v-data-table>
        </v-col>
    </v-row>
</template>

<script>
export default {
    data() {
        return {
            transactions: [
                {
                    date: "2022-01-01",
                    amount: 100,
                    category: "Food",
                    description: "Groceries",
                },
                {
                    date: "2022-01-02",
                    amount: 50,
                    category: "Entertainment",
                    description: "Movie tickets",
                },
                {
                    date: "2022-01-03",
                    amount: 200,
                    category: "Shopping",
                    description: "Clothes",
                },
                {
                    date: "2022-01-03",
                    amount: 150,
                    category: "Transportation",
                    description: "Gasoline",
                },
                {
                    date: "2022-01-04",
                    amount: 20,
                    category: "Food",
                    description: "Coffee",
                },
                {
                    date: "2022-01-05",
                    amount: 30,
                    category: "Food",
                    description: "Lunch",
                },
                {
                    date: "2022-01-06",
                    amount: 40,
                    category: "Entertainment",
                    description: "Concert tickets",
                },
                {
                    date: "2022-01-07",
                    amount: 25,
                    category: "Shopping",
                    description: "Books",
                },
                {
                    date: "2022-01-08",
                    amount: 15,
                    category: "Transportation",
                    description: "Bus fare",
                },
                {
                    date: "2022-01-09",
                    amount: 50,
                    category: "Food",
                    description: "Dinner",
                },
                {
                    date: "2022-01-10",
                    amount: 10,
                    category: "Entertainment",
                    description: "Netflix subscription",
                },
                {
                    date: "2022-01-11",
                    amount: 35,
                    category: "Shopping",
                    description: "Electronics",
                },
                {
                    date: "2022-01-12",
                    amount: 20,
                    category: "Transportation",
                    description: "Taxi",
                },
                {
                    date: "2022-01-13",
                    amount: 15,
                    category: "Food",
                    description: "Snacks",
                },
                {
                    date: "2022-01-14",
                    amount: 30,
                    category: "Entertainment",
                    description: "Video games",
                },
                {
                    date: "2022-01-15",
                    amount: 40,
                    category: "Shopping",
                    description: "Shoes",
                },
                {
                    date: "2022-01-16",
                    amount: 25,
                    category: "Transportation",
                    description: "Train ticket",
                },
                {
                    date: "2022-01-17",
                    amount: 20,
                    category: "Food",
                    description: "Dessert",
                },
                {
                    date: "2022-01-18",
                    amount: 15,
                    category: "Entertainment",
                    description: "Concert tickets",
                },
                {
                    date: "2022-01-19",
                    amount: 30,
                    category: "Shopping",
                    description: "Home decor",
                },
            ],
            newTransaction: { date: "", amount: 0, category: "", description: "" },
        };
    },
    methods: {
        addTransaction() {
            if (this.newTransaction) {
                this.transactions.push(this.newTransaction);
                this.newTransaction = "";
            }
        },
    },
};
</script>
