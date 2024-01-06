import os
from dotenv import load_dotenv
import requests
from terminaltables import AsciiTable

PROGRAMMING_LANGUAGES = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
HH_BASE_URL = "https://api.hh.ru/vacancies"
SJ_BASE_URL = "https://api.superjob.ru/2.0/vacancies"


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


def get_salary_per_language_hh(name):
    page = 0
    processed_count = 0
    average_salary = []
    moscow_id = "1"
    limit_per_page = 50
    vacancies_count = 0
    while True:
        params = {"area": moscow_id,
                  "text": name,
                  "page": page,
                  "per_page": limit_per_page}
        language_response = requests.get(HH_BASE_URL, params=params)
        language_response.raise_for_status()
        vacancies = language_response.json()
        vacancies_count += len(vacancies["items"])
        if vacancies_count >= 2000:
            break
        page += 1
        for vacancy in vacancies["items"]:
            expected_salary = predict_rub_salary_hh(vacancy)
            if expected_salary is None:
                continue
            average_salary.append(expected_salary)
            processed_count += 1
    number_of_vacancies = vacancies["found"]
    print(number_of_vacancies)
    elements_sum = 0
    for element in average_salary:
        elements_sum += element
    average_salary = int(elements_sum / len(average_salary))
    salary_info = {"vacancies_found": number_of_vacancies,
                   "vacancies_processed": processed_count,
                   "average_salary": average_salary
                   }
    return salary_info


def get_salary_per_language_sj(name, token):
    page = 0
    total_number = 0
    processed_count = 0
    average_list = []
    moscow_id = 4
    profession_id = 33
    limit_per_page = 50
    while True:
        headers = {"X-Api-App-Id": token}
        params = {
            "town": moscow_id,
            "catalogues": profession_id,
            "keyword": name,
            "page": page,
            "count": limit_per_page
        }
        language_response = requests.get(SJ_BASE_URL, headers=headers, params=params)
        language_response.raise_for_status()
        vacancies = language_response.json()
        # print(vacancies)
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


def get_sj_table_statistics(sj_languages_salary):
    list_for_table = []
    table_header = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    list_for_table.append(table_header)
    for key, value in sj_languages_salary.items():
        list_for_table.append([key, value["vacancies_found"], value["vacancies_processed"], value["average_salary"]])
    title = "SuperJob Moscow"
    table_instance = AsciiTable(list_for_table, title)
    return table_instance.table


def get_hh_table_statistics(hh_languages_salary):
    list_for_table = []
    table_header = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    list_for_table.append(table_header)
    for key, value in hh_languages_salary.items():
        list_for_table.append([key, value["vacancies_found"], value["vacancies_processed"], value["average_salary"]])
    title = "HeadHunter Moscow"
    table_instance = AsciiTable(list_for_table, title)
    return table_instance.table


def main():
    load_dotenv()
    token = os.environ["SUPERJOB_API_KEY"]
    hh_languages_salary = {}
    for language in PROGRAMMING_LANGUAGES:
        hh_languages_salary[language] = get_salary_per_language_hh(language)
    sj_languages_salary = {}
    for language in PROGRAMMING_LANGUAGES:
        sj_languages_salary[language] = get_salary_per_language_sj(language, token)
    # print(get_hh_table_statistics(hh_languages_salary))
    # print(get_sj_table_statistics(sj_languages_salary))


if __name__ == '__main__':
    main()

