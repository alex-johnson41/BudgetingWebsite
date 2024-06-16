import calendar
import csv

import requests
import json


def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


def create_models(data: list[list[str]]):
    models = []
    for row in data:
        date = row[0].split(' ')[0]
        timestamp = f"{date.split('/')[2]}-{date.split('/')[0].zfill(2)}-{date.split('/')[1].zfill(2)}"
        income_or_expense = row[1]
        income_source = row[2]
        income_amount = row[3]
        type_of_expense = row[4]
        if row[5]:
            expense_amount = 0 - float(row[5])
        month = row[6]

        amount = income_amount if income_or_expense == "Income" else expense_amount
        category = income_source if income_or_expense == "Income" else type_of_expense

        month_num = timestamp.split("-")[1]

        month_name_from_num = calendar.month_name[int(month_num)]
        month_num_from_name = list(calendar.month_name).index(month)

        if month_name_from_num != month:
            timestamp = f"{timestamp.split('-')[0]}-{month_num_from_name:02d}-{timestamp.split('-')[2].zfill(2)}"

        model = {
            "id": None,
            "userID": 0,
            "date": timestamp,
            "amount": amount,
            "category": category
        }
        models.append(model)
    return models


def push_to_table(models):
    for model in models:
        response = requests.post(
            "http://127.0.0.1:8000/transactions/", json=model)
        if response.status_code != 200:
            print(
                f"Failed to push model {model} to the API. Status code: {response.status_code}")
            # Print the response content for debugging purposes
            print(response.content)
    return models


data = read_csv_file(
    "/Users/alexjohnson/SoftwareProjects/BudgetingWebsite/api/raw_data.csv")
models = create_models(data[1:])
push_to_table(models)
