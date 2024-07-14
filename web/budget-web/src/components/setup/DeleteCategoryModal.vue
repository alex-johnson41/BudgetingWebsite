<template>
    <v-dialog max-width="600px">
        <v-card>
            <v-card-title class="text-h5 text-center">Are you sure you want to delete this category? </v-card-title>
            <div v-if="transactionsExist" class="text-center">
                <v-card-text class="wrap-text pa-0">
                    Before deleting, you must select which category all existing
                    <b>{{ category.name }}</b> transactions should be changed to
                </v-card-text>
                <v-row>
                    <v-spacer></v-spacer>
                    <v-col cols="6" class="pb-0">
                        <v-card-text class="pb-0">
                            <v-select
                                class="text-center"
                                width="100%"
                                variant="outlined"
                                v-model="mapTransactionsTo"
                                label="Category"
                                :items="categoriesWithoutDeleted"
                                item-title="name"
                                return-object
                            ></v-select>
                        </v-card-text>
                    </v-col>
                    <v-spacer></v-spacer>
                </v-row>
            </div>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="closeDelete"> Cancel </v-btn>
                <v-btn :disabled="deleteDisabled" color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    name: "ConfirmDeleteModal",
    props: {
        category: {
            type: Object,
            required: true,
        },
        categories: {
            type: Array,
            required: true,
        },
    },
    data: () => ({
        mapTransactionsTo: null,
    }),
    computed: {
        categoriesWithoutDeleted() {
            return this.categories.filter((cat) => cat.id !== this.category.id);
        },
        deleteDisabled() {
            console.log(this.transactionsExist);
            if (this.transactionsExist) {
                return this.mapTransactionsTo == null;
            } else {
                return false;
            }
        },
        transactionsExist() {
            return this.updateTransactionsExist();
        },
    },
    methods: {
        updateTransactionsExist() {
            if (this.category.id != null) {
                const transactions = this.$api.get(`transaction/1/filter?category_id=${this.category.id}`); //TODO: HARD CODED USER ID
                return transactions.length > 0;
            }
            return false;
        },
        closeDelete() {
            this.$emit("closeDelete");
        },
        deleteItemConfirm() {
            this.$emit("deleteItemConfirm");
        },
    },
};
</script>
