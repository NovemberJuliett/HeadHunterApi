import os
from dotenv import load_dotenv
import requests
from terminaltables import AsciiTable, DoubleTable, SingleTable

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
hh_base_url = "https://api.hh.ru/vacancies"
sj_base_url = "https://api.superjob.ru/2.0/vacancies"

load_dotenv()
token = os.environ["SUPERJOB_TOKEN"]


def predict_salary(salary_from, salary_to):
    expected_salary = 0
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    if not salary_from:
        expected_salary = salary_to * 0.8
    if not salary_to:
        expected_salary = salary_from * 1.2
    return expected_salary


def predict_rub_salary_hh(vacancy):
    salary_hh = vacancy["salary"]
    if not salary_hh:
        return None
    salary_hh_from = salary_hh["from"]
    salary_hh_to = salary_hh["to"]
    expected_hh_salary = predict_salary(salary_hh_from, salary_hh_to)
    return expected_hh_salary


def predict_rub_salary_sj(vacancy):
    salary_sj_from = vacancy["payment_from"]
    salary_sj_to = vacancy["payment_to"]
    if salary_sj_from == 0 and salary_sj_to == 0:
        return None
    expected_sj_salary = predict_salary(salary_sj_from, salary_sj_to)
    return expected_sj_salary


def salary_info_per_language_hh(name):
    page = 0
    total_number = 0
    processed_count = 0
    average_list = []
    while True:
        params = {"area": "1",
                  "text": name,
                  "page": page,
                  "per_page": 100}
        language_response = requests.get(hh_base_url, params=params)
        if language_response.status_code != 200:
            break
        vacancies = language_response.json()
        list_vacancies = vacancies["items"]
        number_of_vacancies = len(list_vacancies)
        if number_of_vacancies == 0:
            break
        total_number = total_number + number_of_vacancies
        page += 1
        for vacancy in list_vacancies:
            expected_salary = predict_rub_salary_hh(vacancy)
            if expected_salary is None:
                continue
            average_list.append(expected_salary)
            processed_count += 1
    elements_sum = 0
    for element in average_list:
        elements_sum += element
    average_salary = int(elements_sum / len(average_list))
    salary_info = {"vacancies_found": total_number,
                   "vacancies_processed": processed_count,
                   "average_salary": average_salary
                   }
    return salary_info


# hh_languages_salary = {}
# for language in languages_list:
#     hh_languages_salary[language] = salary_info_per_language_hh(language)


def salary_info_per_language_sj(name):
    page = 0
    total_number = 0
    processed_count = 0
    average_list = []
    while True:
        headers = {"X-Api-App-Id": token}
        params = {
            "town": 4,
            "catalogues": 33,
            "keyword": name,
            "page": page,
            "count": 50
        }
        language_response = requests.get(sj_base_url, headers=headers, params=params)
        if language_response.status_code != 200:
            break
        vacancies = language_response.json()
        list_vacancies = vacancies["objects"]
        number_of_vacancies = len(list_vacancies)
        if number_of_vacancies == 0:
            break
        total_number = total_number + number_of_vacancies
        page += 1
        for vacancy in list_vacancies:
            expected_salary = predict_rub_salary_sj(vacancy)
            if expected_salary is None:
                continue
            average_list.append(expected_salary)
            processed_count += 1
    elements_sum = 0
    if not average_list:
        return {"vacancies_found": total_number,
                "vacancies_processed": 0,
                "average_salary": None
                }
    for element in average_list:
        elements_sum += element
    average_salary = int(elements_sum / len(average_list))
    salary_info = {"vacancies_found": total_number,
                   "vacancies_processed": processed_count,
                   "average_salary": average_salary
                   }
    return salary_info


# sj_languages_salary = {}
# for language in languages_list:
#     sj_languages_salary[language] = salary_info_per_language_sj(language)
# # print(sj_languages_salary)

test_dict = {"Python": {"vacancies_found": 2, "vacancies_processed": 5, "average_salary": 40000},
             "Java": {"vacancies_found": 5, "vacancies_processed": 7, "average_salary": 70000}}

TABLE_DATA = [
    ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"],
    ["Python", 2, 3, 40000],
    ["Java", 5, 6, 70000]
]

TABLE_DATA_2 = [
    ["Язык программирования"],
    ["Python"],
    ["Java"]
]

TABLE_DATA_3 = [
    ["Язык программирования","Вакансий найдено"],
    ["Python", 2],
    ["Java", 5]
]


def get_list(salary_info):
    list = []
    table = ["Язык программирования", "Вакансий найдено"]
    list.append(table)
    for key, value in salary_info.items():
        list.append([key, value["vacancies_found"]])
    return list

print(get_list(test_dict))


# def sj_table_statistics():
#     title = "SuperJob Moscow"
#     table_instance = AsciiTable(TABLE_DATA_3, title)
#     return table_instance.table
#
# print(sj_table_statistics())

