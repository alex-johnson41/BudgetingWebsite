<template>
    <v-main>
        <v-container>
            <v-row>
                <v-col cols="12">
                    <h1>Transactions</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                    <v-card>
                        <v-card-title>Transactions</v-card-title>
                        <v-card-text>
                            <v-table>
                                <template v-slot:default>
                                    <thead>
                                        <tr>
                                            <th class="text-left">Date</th>
                                            <th class="text-left">Description</th>
                                            <th class="text-left">Amount</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr
                                            v-for="transaction in transactions"
                                            :key="transaction.id"
                                        >
                                            <td>{{ transaction.date }}</td>
                                            <td>{{ transaction.description }}</td>
                                            <td>{{ transaction.amount }}</td>
                                        </tr>
                                    </tbody>
                                </template>
                            </v-table>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<script>
export default {
    data() {
        return {
            transactions: [
                {
                    id: 1,
                    date: '2021-01-01',
                    description: 'Groceries',
                    amount: 100.0
                },
                {
                    id: 2,
                    date: '2021-01-02',
                    description: 'Gas',
                    amount: 50.0
                },
                {
                    id: 3,
                    date: '2021-01-03',
                    description: 'Dinner',
                    amount: 25.0
                }
            ]
        }
    }
}
</script>
