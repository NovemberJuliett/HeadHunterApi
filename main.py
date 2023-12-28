import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
token = os.environ["SUPERJOB_TOKEN"]
url = "https://api.superjob.ru/2.0/vacancies"


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    if not salary_from:
        expected_salary = salary_to * 0.8
    if not salary_to:
        expected_salary = salary_from * 1.2
    return expected_salary


def predict_rub_salary_sj(vacancy):
    headers = {"X-Api-App-Id": token}
    params = {
        "town": 4,
        "catalogues": 33}
    response = requests.get(url, headers=headers, params=params)
    salary_data = response.json()
    salary = salary_data["objects"]
    if not salary:
        return None
    for vacancy in salary:
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
        expected_salary = int(predict_salary(salary_from, salary_to))
    return expected_salary
    # objects =
    # for item in objects:
    #     print(item["profession"]+",", item["town"]["title"])


print(predict_rub_salary_sj(1))