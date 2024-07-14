<template>
    <v-dialog max-width="500px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ this.formTitle }}</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12" md="6" sm="6">
                            <v-text-field variant="outlined" v-model="item.name" label="Name"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" sm="6">
                            <v-select
                                variant="outlined"
                                v-model="item.is_income"
                                label="Income Or Expense"
                                :items="incomeOrExpense"
                                item-title="name"
                                return-object
                            ></v-select>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="close()"> Cancel </v-btn>
                <v-btn color="blue-darken-1" variant="text" @click="save()"> Save </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: "EditTransactionModal",
    props: {
        editedCategory: Object,
        formTitle: String,
        categories: Array,
    },
    data: () => ({
        incomeOrExpense: [
            { name: "Income", value: true },
            { name: "Expense", value: false },
        ],
    }),
    computed: {
        item() {
            return this.editedCategory;
        },
    },
    methods: {
        close() {
            this.$emit("close");
        },
        save() {
            this.item.is_income = this.item.is_income.value;
            this.$emit("save", Object.assign({}, this.item));
        },
    },
};
</script>
