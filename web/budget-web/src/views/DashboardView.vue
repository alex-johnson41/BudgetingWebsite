<template>
    <v-container fluid v-if="dataInitialized" class="ma-0 pa-0">
        <v-row style="height: 50%" class="mt-3 ml-3" no-gutters>
            <v-col cols="3">
                <overview-pod :transactions="transactions" :budgets="budgets" />
            </v-col>
            <v-col cols="3"></v-col>
            <v-col cols="6"></v-col>
        </v-row>
        <v-row style="height: 50%" no-gutters>
            <v-col cols="3"></v-col>
            <v-col cols="9"></v-col>
        </v-row>
    </v-container>
</template>
<script>
import OverviewPod from "@/components/dashboard/OverviewPod.vue";

export default {
    components: {
        OverviewPod,
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
<style scoped>
.half-screen-height {
    height: 45vh;
    overflow: hidden;
}
</style>
