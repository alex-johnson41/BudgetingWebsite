<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-row class="pt-0 mt-10" justify="center">
        <v-col cols="6">
            <v-data-table
                :headers="headers"
                :items="transactions"
                :sort-by="[{ key: 'date', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>Recent Transactions</v-toolbar-title>
                        <v-spacer />
                        <edit-transaction-modal
                            v-model="dialog"
                            :editedItem="editedItem"
                            :formTitle="formTitle"
                            @close="close"
                            @save="save"
                        />
                        <delete-transaction-modal
                            v-model="dialogDelete"
                            :editedItem="editedItem"
                            @closeDelete="closeDelete"
                            @deleteItemConfirm="deleteItemConfirm"
                        />
                    </v-toolbar>
                </template>
                <template v-slot:item.amount="{ item }"> ${{ item.amount }} </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon class="me-2" size="small" @click="editItem(item)"> mdi-pencil </v-icon>
                    <v-icon size="small" @click="deleteItem(item)"> mdi-delete </v-icon>
                </template>
                <template v-slot:no-data>
                    <v-btn color="primary" @click="initialize"> Reset </v-btn>
                </template>
            </v-data-table>
        </v-col>
    </v-row>
</template>
<script>
import EditTransactionModal from "@/components/EditTransactionModal.vue";
import DeleteTransactionModal from "@/components/DeleteTransactionModal.vue";
// TODO: Make each row red or green for income or expense
// Make category field a dropdown
export default {
    components: {
        EditTransactionModal,
        DeleteTransactionModal,
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
        editedIndex: -1,
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
            return this.editedIndex === -1 ? "New Item" : "Edit Item";
        },
    },
    created() {
        this.initialize();
    },

    methods: {
        initialize() {
            this.transactions = [
                {
                    date: "2021-10-01",
                    amount: 100,
                    category: "Groceries",
                    description: "Aldi",
                },
                {
                    date: "2021-10-02",
                    amount: 50,
                    category: "Shopping",
                    description: "Amazon",
                },
                {
                    date: "2021-10-03",
                    amount: 20,
                    category: "Entertainment",
                    description: "Movie tickets",
                },
                {
                    date: "2021-10-04",
                    amount: 75,
                    category: "Dining",
                    description: "Restaurant",
                },
                {
                    date: "2021-10-05",
                    amount: 30,
                    category: "Transportation",
                    description: "Gas station",
                },
                {
                    date: "2021-10-06",
                    amount: 15,
                    category: "Groceries",
                    description: "Supermarket",
                },
                {
                    date: "2021-10-07",
                    amount: 50,
                    category: "Shopping",
                    description: "Online store",
                },
                {
                    date: "2021-10-08",
                    amount: 10,
                    category: "Entertainment",
                    description: "Concert tickets",
                },
                {
                    date: "2021-10-09",
                    amount: 40,
                    category: "Dining",
                    description: "Fast food",
                },
                {
                    date: "2021-10-10",
                    amount: 25,
                    category: "Transportation",
                    description: "Bus fare",
                },
                {
                    date: "2021-10-11",
                    amount: 60,
                    category: "Shopping",
                    description: "Department store",
                },
            ];
        },

        editItem(item) {
            this.editedIndex = this.transactions.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialog = true;
        },

        deleteItem(item) {
            this.editedIndex = this.transactions.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },

        deleteItemConfirm() {
            this.transactions.splice(this.editedIndex, 1);
            this.closeDelete();
        },

        close() {
            this.dialog = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            });
        },

        closeDelete() {
            this.dialogDelete = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            });
        },

        save(item) {
            if (this.editedIndex > -1) {
                Object.assign(this.transactions[this.editedIndex], item);
            } else {
                this.transactions.push(item);
            }
            this.close();
        },
    },
};
</script>
