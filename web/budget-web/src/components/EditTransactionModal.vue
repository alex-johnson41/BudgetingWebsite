<template>
    <v-dialog max-width="500px">
        <template v-slot:activator="{ props }">
            <v-btn class="mb-2" color="primary" dark v-bind="props">
                <v-icon class="pr-3"> mdi-plus-box </v-icon>
                New Transaction
            </v-btn>
        </template>
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ this.formTitle }}</span>
            </v-card-title>

            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12" md="4" sm="6">
                            <v-date-input
                                variant="outlined"
                                v-model="itemDate"
                                label="Select a date"
                                prepend-icon=""
                            ></v-date-input>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                            <v-text-field
                                variant="outlined"
                                v-model="item.amount"
                                label="Amount"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                            <v-text-field
                                variant="outlined"
                                v-model="item.category"
                                label="Category"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                            <v-text-field
                                variant="outlined"
                                v-model="item.description"
                                label="Description"
                            ></v-text-field>
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
import { VDateInput } from "vuetify/lib/labs/components.mjs";
export default {
    name: "EditTransactionModal",
    components: {
        VDateInput,
    },
    props: {
        editedItem: Object,
        formTitle: String,
    },
    data() {
        return {
            date: new Date(),
        };
    },
    computed: {
        item() {
            return this.editedItem;
        },
        itemDate: {
            get() {
                if (!this.item.date) {
                    return new Date();
                }
                return new Date(this.item.date + "T00:00:00") || new Date();
            },
            set(value) {
                this.item.date = value.toISOString().split("T")[0];
            },
        },
    },
    methods: {
        close() {
            this.$emit("close");
        },
        save() {
            this.$emit("save", Object.assign({}, this.item));
        },
    },
};
</script>
