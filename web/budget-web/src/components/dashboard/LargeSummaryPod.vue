<template>
    <v-card class="half-screen-card">
        <v-card-title class="title-container"> Spending Breakdown </v-card-title>
        <v-card-text class="flex-column">
            <v-row>
                <v-col cols="6" class="d-flex justify-center">
                    <Chart
                        type="doughnut"
                        :data="chartData"
                        :options="chartOptions"
                        class="chart-container w-full md:w-[30rem]"
                    />
                    <div class="text-center total-spent">
                        <p class="text-h6">Total Spent:</p>
                        <p class="text-h4">{{ displayValue(totalSpent) }}</p>
                    </div>
                </v-col>
                <v-col cols="6">
                    <div class="category-list">
                        <div v-for="category in categories" :key="category.id">
                            <v-row v-if="calculateTotal(category.id) > 0 && category.is_income == false">
                                <v-col cols="2">
                                    <div class="square pa-0" :style="{ backgroundColor: category.color }"></div>
                                </v-col>
                                <v-col cols="6"> {{ category.name }} </v-col>
                                <v-col cols="4"> {{ displayValue(calculateTotal(category.id)) }} </v-col>
                            </v-row>
                        </div>
                    </div>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
import { displayValue } from "@/utilities.js";
import Chart from "primevue/chart";

export default {
    components: {
        Chart,
    },
    props: {
        transactions: {
            type: Array,
            required: true,
        },
        categories: {
            type: Array,
            required: true,
        },
    },
    mounted() {
        this.assignCategoryColors();
    },
    computed: {
        totalSpent() {
            return this.transactions
                .filter((transaction) => {
                    const category = this.categories.find((cat) => cat.id === transaction.category_id);
                    return category && !category.is_income;
                })
                .reduce((acc, transaction) => acc + transaction.amount, 0);
        },
        expenseCategories() {
            return this.categories.filter((category) => !category.is_income);
        },
        chartData() {
            return {
                labels: this.expenseCategories.map((category) => category.name),
                datasets: [
                    {
                        data: this.expenseCategories.map((category) => this.calculateTotal(category.id)),
                        backgroundColor: this.expenseCategories.map((category) => category.color),
                    },
                ],
            };
        },
        chartOptions() {
            return {
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                cutout: "75%",
            };
        },
    },
    methods: {
        calculateTotal(categoryId) {
            return this.transactions
                .filter((transaction) => transaction.category_id === categoryId)
                .reduce((acc, transaction) => acc + transaction.amount, 0);
        },
        assignCategoryColors() {
            const colors = [
                "#FF5733",
                "#33FF57",
                "#3357FF",
                "#FF33A1",
                "#A133FF",
                "#33FFF5",
                "#FF9933",
                "#33FFC7",
                "#33A1FF",
                "#FF33E5",
                "#33FFA1",
            ];
            this.categories.forEach((category, index) => {
                category.color = colors[index % colors.length];
            });
        },
        displayValue(value) {
            return displayValue(value);
        },
        setChartOptions() {
            return {
                legend: {
                    display: false,
                },
            };
        },
    },
};
</script>
<style scoped lang="scss">
@import "@/styles.scss";
.half-screen-card {
    height: 42vh;
    display: flex;
    flex-direction: column;
    background-color: lightgray;
    border-radius: 20px;
}
.square {
    width: 20px;
    height: 20px;
    border: 1px solid #ccc;
    margin: auto;
}
.chart-container {
    z-index: 10;
    height: 35vh;
}
.category-list {
    max-height: 80%;
    overflow-y: auto;
    overflow-x: hidden;
}
.total-spent {
    position: absolute;
    top: 40%;
    left: 14.5%;
}
</style>
