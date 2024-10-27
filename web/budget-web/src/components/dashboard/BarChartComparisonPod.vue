<template>
    <v-card class="half-screen-card">
        <v-card-title class="title-container"> Budgeted vs. Actual </v-card-title>
        <v-card-text class="flex-column chart-container">
            <Chart type="bar" :data="chartData" :options="chartOptions" />
        </v-card-text>
    </v-card>
</template>

<script>
import Chart from "primevue/chart";
export default {
    components: {
        Chart,
    },
    props: {
        budgets: {
            type: Array,
            required: true,
        },
        categories: {
            type: Array,
            required: true,
        },
        transactions: {
            type: Array,
            required: true,
        },
    },
    watch: {
        budgets: {
            handler() {
                this.chartData = this.setChartData();
            },
            deep: true,
        },
        transactions: {
            handler() {
                this.chartData = this.setChartData();
            },
            deep: true,
        },
    },
    data() {
        return {
            chartData: null,
            chartOptions: null,
        };
    },
    mounted() {
        this.chartData = this.setChartData();
        this.chartOptions = this.setChartOptions();
    },
    methods: {
        createChartData() {
            console.log(this.categories);
            return this.categories
                .filter(
                    (category) =>
                        !category.is_income && this.budgets.find((budget) => budget.category_id == category.id).amount > 0
                )
                .map((category) => {
                    return {
                        label: category.name,
                        budgeted: this.budgets.find((budget) => budget.category_id == category.id).amount,
                        actual: this.transactions
                            .filter((transaction) => transaction.category_id == category.id)
                            .reduce((acc, transaction) => acc + transaction.amount, 0),
                    };
                });
        },
        setChartData() {
            let data = this.createChartData();
            console.log(data);
            return {
                labels: data.map((category) => category.label),
                datasets: [
                    {
                        label: "Budgeted",
                        backgroundColor: "#2196F3", // Blue color
                        borderColor: "#2196F3", // Blue color
                        data: data.map((category) => category.budgeted),
                    },
                    {
                        label: "Actual",
                        backgroundColor: "#FF9800", // Orange color
                        borderColor: "#FF9800", // Orange color
                        data: data.map((category) => category.actual),
                    },
                ],
            };
        },
        setChartOptions() {
            const documentStyle = getComputedStyle(document.documentElement);
            const textColor = documentStyle.getPropertyValue("--p-text-color");
            const textColorSecondary = documentStyle.getPropertyValue("--p-text-muted-color");
            const surfaceBorder = documentStyle.getPropertyValue("--p-content-border-color");

            return {
                maintainAspectRatio: false,
                aspectRatio: 1,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || "";
                                if (label) {
                                    label += ": ";
                                }
                                label += "$" + context.raw.toFixed(2);
                                return label;
                            },
                        },
                    },
                    legend: {
                        labels: {
                            color: textColor,
                        },
                    },
                },
                scales: {
                    x: {
                        ticks: {
                            color: textColorSecondary,
                            font: {
                                weight: 500,
                            },
                        },
                        grid: {
                            display: false,
                            drawBorder: false,
                        },
                    },
                    y: {
                        ticks: {
                            color: textColorSecondary,
                        },
                        grid: {
                            color: surfaceBorder,
                            drawBorder: false,
                        },
                    },
                },
            };
        },
    },
};
</script>

<style scoped>
.half-screen-card {
    height: 42vh;
    display: flex;
    flex-direction: column;
    background-color: lightgray;
    border-radius: 20px;
}
.chart-container {
    height: 100%;
}

.chart-container .p-chart {
    height: 100%;
}
</style>
