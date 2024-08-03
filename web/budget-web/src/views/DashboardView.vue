<template>
    <v-container fluid v-if="dataInitialized" class="ma-0 pa-0">
        <v-row class="ma-0 pa-0" no-gutters>
            <v-col cols="3" class="pa-2">
                <overview-pod :transactions="transactions" :budgets="budgets" />
            </v-col>
            <v-col cols="3" class="pa-2">
                <small-summary-pod />
            </v-col>
            <v-col cols="6" class="pa-2">
                <large-summary-pod />
            </v-col>
        </v-row>
        <v-row class="ma-0 pa-0" no-gutters>
            <v-col cols="3" class="pa-2">
                <small-summary-pod />
            </v-col>
            <v-col cols="9" class="pa-2">
                <bar-chart-comparison-pod :budgets="budgets" :categories="categories" :transactions="transactions" />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import OverviewPod from "@/components/dashboard/OverviewPod.vue";
import BarChartComparisonPod from "@/components/dashboard/BarChartComparisonPod.vue";
import LargeSummaryPod from "@/components/dashboard/LargeSummaryPod.vue";
import SmallSummaryPod from "@/components/dashboard/SmallSummaryPod.vue";

export default {
    components: {
        OverviewPod,
        BarChartComparisonPod,
        LargeSummaryPod,
        SmallSummaryPod,
    },
    data: () => ({
        budgets: [],
        categories: [],
        transactions: [],
        selectedMonth: new Date().getMonth(),
        selectedYear: new Date().getFullYear(),
        dataInitialized: false,
    }),
    computed: {},
    mounted() {
        this.initializeData();
    },
    methods: {
        initializeData() {
            Promise.all([
                this.$api.get("category/user/1").then((response) => {
                    this.categories = response;
                }), // TODO: HARD CODED USER ID
                this.$api.get(`budget/user/1/filter?year=${this.selectedYear}&month=${this.selectedMonth}`).then((response) => {
                    this.budgets = response;
                }), // TODO: HARD CODED USER ID
                this.$api.get(`transaction/1/filter?year=${this.selectedYear}&month=${this.selectedMonth}`).then((response) => {
                    this.transactions = response;
                }), // TODO: HARD CODED USER ID
            ]).then(() => {
                this.dataInitialized = true;
            });
        },
    },
};
</script>
<style scoped>
.half-screen-height {
    height: 45vh;
    overflow: hidden;
}
</style>
