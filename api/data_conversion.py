import calendar
import csv

import requests


def read_csv_file(file_path) -> list[list[str]]:
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


def create_categories(data: list[list[str]]):
    categories = []
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

        is_income = income_or_expense == "Income"
        type = income_source if income_or_expense == "Income" else type_of_expense

        category = {
            "name": type,
            "is_income": is_income,
            "user_id": 1
        }
        if category["name"] not in [c["name"] for c in categories]:
            categories.append(category)

    return categories


def create_models(data: list[list[str]]):
    models = []
    for row in data:
        date = row[0].split(' ')[0]
        timestamp = f"{date.split('/')[2]}-{date.split('/')[0].zfill(2)}-{date.split('/')[1].zfill(2)}"
        income_or_expense = row[1]
        income_source = row[2]
        income_amount = row[3]
        type_of_expense = row[4]
        expense_amount = row[5]
        month = row[6]

        amount = float(income_amount) if income_or_expense == "Income" else float(
            expense_amount)
        category_name = income_source if income_or_expense == "Income" else type_of_expense
        category = requests.get(
            f"http://127.0.0.1:8000/category/1/{category_name}").json()

        month_num = timestamp.split("-")[1]

        month_name_from_num = calendar.month_name[int(month_num)]
        month_num_from_name = list(calendar.month_name).index(month)

        if month_name_from_num != month:
            timestamp = f"{timestamp.split('-')[0]}-{month_num_from_name:02d}-{timestamp.split('-')[2].zfill(2)}"

        model = {
            "user_id": 1,
            "date": timestamp,
            "amount": amount,
            "category_id": category["id"]
        }
        models.append(model)
    return models


def push_to_table(models, route):
    for model in models:
        response = requests.post(
            f"http://127.0.0.1:8000/{route}", json=model)
        if response.status_code != 200:
            print(
                f"Failed to push model {model} to the API. Status code: {response.status_code}")
            print(response.content)
    return models


data = read_csv_file(
    "/Users/alexjohnson/SoftwareProjects/BudgetingWebsite/api/raw_data.csv")
categories = create_categories(data[1:])
push_to_table(categories, "category")
models = create_models(data[1:])
push_to_table(models, "transaction")
