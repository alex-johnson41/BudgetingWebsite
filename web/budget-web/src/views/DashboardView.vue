<template class="background">
    <v-container fluid v-if="dataInitialized" class="ma-0 pa-0 dashboard">
        <v-row class="ma-0 pa-0" no-gutters>
            <v-col cols="3" class="pa-2">
                <overview-pod :transactions="transactions" :budgets="budgets" class="pod" />
            </v-col>
            <v-col cols="3" class="pa-2">
                <small-summary-pod class="pod" />
            </v-col>
            <v-col cols="6" class="pa-2">
                <large-summary-pod class="pod" :transactions="transactions" :categories="categories" />
            </v-col>
        </v-row>
        <v-row class="ma-0 pa-0" no-gutters>
            <v-col cols="3" class="pa-2">
                <small-summary-pod class="pod" />
            </v-col>
            <v-col cols="9" class="pa-2">
                <bar-chart-comparison-pod :budgets="budgets" :categories="categories" :transactions="transactions" class="pod" />
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
        selectedMonth: new Date().getMonth() + 1,
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
<style scoped lang="scss">
@import "@/styles.scss";
.half-screen-height {
    height: 45vh;
    overflow: hidden;
}
.pod {
    background-color: $secondary;
}
</style>
