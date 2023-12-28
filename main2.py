from pprint import pprint

import requests

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = "https://api.hh.ru/vacancies"


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    if not salary_from:
        expected_salary = salary_to * 0.8
    if not salary_to:
        expected_salary = salary_from * 1.2
    return expected_salary


def predict_rub_salary_hh(vacancy):
    salary_response = requests.get(base_url)





def salary_info_per_language(name):
    page = 0
    total_number = 0
    processed_count = 0
    average_list = []

    while True:
        params = {"area": "1",
                  "text": name,
                  "page": page,
                  "per_page": 100}
        language_response = requests.get(base_url, params=params)
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
            salary = vacancy["salary"]
            if not salary:
                continue
            salary_from = salary["from"]
            salary_to = salary["to"]
            expected_salary = predict_salary(salary_from, salary_to)
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


result_languages_salary = {}
for language in languages_list:
    result_languages_salary[language] = salary_info_per_language(language)
print(result_languages_salary)
