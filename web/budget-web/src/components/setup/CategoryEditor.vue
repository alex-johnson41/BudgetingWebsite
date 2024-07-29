<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-card elevation="0" class="ma-0 pa-0">
        <v-card-title style="font-size: 30px">Customize your categories</v-card-title>
        <v-card-text>
            <v-row class="pt-0 mt-2" justify="center">
                <v-col cols="8">
                    <v-data-table-virtual
                        density="compact"
                        height="450px"
                        :headers="headers"
                        :items="categories"
                        :sort-by="[{ key: 'name', order: 'asc' }]"
                    >
                        <template v-slot:top>
                            <v-toolbar flat>
                                <v-toolbar-title>Categories</v-toolbar-title>
                                <v-spacer />
                                <v-btn @click="openEditCategoryModal" variant="outlined" class="mr-5" color="primary" dark>
                                    <v-icon class="pr-3"> mdi-plus-box </v-icon>
                                    New Category
                                </v-btn>
                                <edit-category-modal
                                    v-model="dialog"
                                    :editedCategory="editedItem"
                                    :formTitle="formTitle"
                                    :categories="categories"
                                    @close="closeEditModal"
                                    @save="saveEditedOrNewItem"
                                />
                                <delete-category-modal
                                    v-model="dialogDelete"
                                    :categories="categories"
                                    :category="editedItem"
                                    :transactions="transactions"
                                    @closeDelete="closeDeleteModal"
                                    @deleteItemConfirm="deleteConfirmed"
                                />
                            </v-toolbar>
                        </template>
                        <template v-slot:item.name="{ item }">
                            {{ item.name }}
                        </template>
                        <template v-slot:item.is_income="{ item }">
                            {{ item.is_income ? "Income" : "Expense" }}
                        </template>
                        <template v-slot:item.actions="{ item }">
                            <v-icon class="me-2" size="small" @click="openEditCategoryModal(item)"> mdi-pencil </v-icon>
                            <v-icon size="small" @click="openDeleteCategoryModal(item)"> mdi-delete </v-icon>
                        </template>
                    </v-data-table-virtual>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import EditCategoryModal from "@/components/setup/EditCategoryModal.vue";
import DeleteCategoryModal from "@/components/setup/DeleteCategoryModal.vue";

export default {
    components: {
        EditCategoryModal,
        DeleteCategoryModal,
    },
    data: () => ({
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                title: "Category",
                align: "start",
                sortable: true,
                key: "name",
            },
            { title: "Income or Expense", key: "is_income" },
            { title: "Actions", key: "actions", sortable: false },
        ],
        categories: [],
        editedId: -1,
        editedItem: {
            name: "",
            is_income: undefined,
        },
        defaultItem: {
            name: "",
            is_income: undefined,
        },
        transactions: [],
    }),

    computed: {
        formTitle() {
            return this.editedId === -1 ? "New Category" : "Edit Category";
        },
    },
    mounted() {
        this.refreshTable();
    },

    methods: {
        refreshTable() {
            this.$api.get("category/user/1").then((response) => {
                this.categories = response;
            }); // TODO: HARD CODED USER ID
        },
        openEditCategoryModal(item) {
            this.editedId = item.id || -1;
            this.editedItem = Object.assign({}, item);
            this.dialog = true;
        },

        async openDeleteCategoryModal(item) {
            this.transactions = await this.$api.get(`transaction/1/filter?category_id=${item.id}`);
            this.editedId = item.id || -1;
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },

        deleteConfirmed() {
            this.$api.delete(`category/${this.editedItem.id}`).then(() => {
                this.refreshTable();
                this.closeDeleteModal();
            });
        },

        closeEditModal() {
            this.dialog = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedId = -1;
            });
        },

        closeDeleteModal() {
            this.dialogDelete = false;
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedId = -1;
            });
        },

        async saveEditedOrNewItem(item) {
            if (this.editedId > -1) {
                this.$api.patch(`category/${item.id}`, item).then(() => {
                    this.refreshTable();
                    this.closeEditModal();
                });
            } else {
                item.user_id = 1; // TODO: HARD CODED USER ID
                this.$api.post("category", item).then(() => {
                    this.refreshTable();
                    this.closeEditModal();
                });
            }
        },
    },
};
</script>
