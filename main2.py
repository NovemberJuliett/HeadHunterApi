from pprint import pprint

import requests

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = "https://api.hh.ru/vacancies"


def get_salary_statistics(name):
    page = 0
    salary_info_dict = {}
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
            if salary_from and salary_to:
                expected_salary = (salary_from + salary_to) / 2
            if not salary_from:
                expected_salary = salary_to * 0.8
            if not salary_to:
                expected_salary = salary_from * 1.2
            average_list.append(expected_salary)
            processed_count += 1
            elements_sum = 0
            for element in average_list:
                elements_sum += element
    average_salary = int(elements_sum / len(average_list))
    salary_info_dict[name] = {"vacancies_found": total_number,
                                      "vacancies_processed": processed_count,
                                      "average_salary": average_salary
                                      }
    return salary_info_dict


print(get_salary_statistics("Shell"))
