<template>
    <v-card class="half-screen-card">
        <v-card-title class="title-container"> Spending Summary </v-card-title>
        <v-card-text class="flex-column">
            <v-row>
                <v-col cols="12" class="d-flex justify-center pb-0">
                    <Chart
                        type="doughnut"
                        :data="chartData"
                        :options="chartOptions"
                        class="chart-container w-full md:w-[30rem]"
                    />
                    <div class="text-center total-spent">
                        <p class="text-h8">Total Spent:</p>
                        <p class="text-h6">{{ displayValue(totalSpent) }}</p>
                    </div>
                </v-col>
                <v-col cols="12" class="pt-0">
                    <div class="category-list">
                        <div v-for="group in expenseGroups" :key="group.color">
                            <v-row v-if="calculateTotal(group.name) > 0">
                                <v-col cols="2">
                                    <div class="square pa-0" :style="{ backgroundColor: group.color }"></div>
                                </v-col>
                                <v-col cols="6"> {{ group.name }} </v-col>
                                <v-col cols="4"> {{ displayValue(calculateTotal(group.name)) }} </v-col>
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
import _ from "underscore";
import * as cloneDeep from "lodash.clonedeep";

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
    watch: {
        transactions: {
            handler() {
                this.assignCategoryColors();
            },
            deep: true,
        },
    },
    computed: {
        expenseGroups() {
            const groups = _.uniq(this.expenseCategories.map((category) => category.group));
            return groups.map((group) => ({
                name: group,
            }));
        },
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
            this.assignCategoryColors();
            return {
                labels: this.expenseGroups.map((group) => group.name),
                datasets: [
                    {
                        data: this.expenseGroups.map((group) => (this.calculateTotal(group.name) / this.totalSpent) * 100),
                        backgroundColor: this.expenseGroups.map((group) => group.color),
                    },
                ],
            };
        },
        chartOptions() {
            return {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || "";
                                if (label) {
                                    label += ": ";
                                }
                                label += context.raw.toFixed(2) + "%";
                                return label;
                            },
                        },
                    },
                    legend: {
                        display: false,
                    },
                },
                cutout: "75%",
            };
        },
    },
    methods: {
        calculateTotal(group) {
            return this.transactions
                .filter((transaction) => {
                    const category = this.categories.find((cat) => cat.id === transaction.category_id);
                    return category && !category.is_income && category.group === group;
                })
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
            this.expenseGroups.forEach((group, index) => {
                group.color = colors[index % colors.length];
            });
        },
        displayValue(value) {
            return displayValue(value);
        },
    },
};
</script>
<style scoped>
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
    height: 25vh;
}
.category-list {
    max-height: 60%;
    overflow-y: auto;
    overflow-x: hidden;
}
.total-spent {
    position: absolute;
    top: 35%;
    left: 37%;
}
</style>
