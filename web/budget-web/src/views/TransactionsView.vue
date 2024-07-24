<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-row class="pt-0 mt-10" justify="center">
        <v-col cols="6">
            <v-data-table :headers="headers" :items="transactions" :sort-by="[{ key: 'date', order: 'desc' }]">
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>Recent Transactions</v-toolbar-title>
                        <v-spacer />
                        <v-btn @click="editItem" variant="outlined" class="mr-5" color="primary" dark>
                            <v-icon class="pr-3"> mdi-plus-box </v-icon>
                            New Transaction
                        </v-btn>
                        <edit-transaction-modal
                            v-model="dialog"
                            :editedItem="editedItem"
                            :formTitle="formTitle"
                            :categories="categories"
                            @close="close"
                            @save="save"
                        />
                        <confirm-delete-modal
                            v-model="dialogDelete"
                            @closeDelete="closeDelete"
                            @deleteItemConfirm="deleteItemConfirm"
                        />
                    </v-toolbar>
                </template>
                <template v-slot:item.amount="{ item }">
                    <v-chip :color="item.category.is_income ? 'green' : 'red'" dark> ${{ item.amount }} </v-chip>
                </template>
                <template v-slot:item.category="{ item }"> {{ item.category.name }} </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon class="me-2" size="small" @click="editItem(item)"> mdi-pencil </v-icon>
                    <v-icon size="small" @click="deleteItem(item)"> mdi-delete </v-icon>
                </template>
            </v-data-table>
        </v-col>
    </v-row>
</template>
<script>
import EditTransactionModal from "@/components/EditTransactionModal.vue";
import ConfirmDeleteModal from "@/components/ConfirmDeleteModal.vue";

export default {
    components: {
        EditTransactionModal,
        ConfirmDeleteModal,
    },
    data: () => ({
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                title: "Date",
                align: "start",
                sortable: true,
                key: "date",
            },
            { title: "Amount", key: "amount" },
            { title: "Category", key: "category" },
            { title: "Description", key: "description" },
            { title: "Actions", key: "actions", sortable: false },
        ],
        transactions: [],
        categories: [],
        editedId: -1,
        editedItem: {
            date: "",
            amount: 0,
            category: "",
            description: "",
        },
        defaultItem: {
            date: "",
            amount: 0,
            category: "",
            description: "",
        },
    }),

    computed: {
        formTitle() {
            return this.editedId === -1 ? "New Item" : "Edit Item";
        },
    },
    async mounted() {
        await this.refreshTable();
    },

    methods: {
        async refreshTable() {
            this.categories = await this.$api.get("category/user/1"); // TODO: HARD CODED USER ID
            this.transactions = await this.$api.get("transaction/user/1"); //TODO: HARD CODED USER ID
        },

        editItem(item) {
            this.editedId = item.id || -1;
            this.editedItem = Object.assign({}, item);
            this.dialog = true;
        },

        deleteItem(item) {
            this.editedId = item.id || -1;
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },

        deleteItemConfirm() {
            this.$api.delete(`transaction/${this.editedItem.id}`);
            this.refreshTable();
            this.closeDelete();
        },

        close() {
            this.dialog = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedId = -1;
            });
        },

        closeDelete() {
            this.dialogDelete = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedId = -1;
            });
        },

        async save(item) {
            if (this.editedId > -1) {
                await this.$api.patch(`transaction/${item.id}`, item);
            } else {
                item.category_id = item.category.id;
                item.user_id = 1; // TODO: HARD CODED USER ID
                await this.$api.post("transaction", item);
            }
            await this.refreshTable();
            this.close();
        },
    },
};
</script>
