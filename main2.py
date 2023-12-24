from pprint import pprint

import requests

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]

page = 0
per_page = 100

base_url = "https://api.hh.ru/vacancies"

salary_info_dict = {}
total_number = 0
processed_count = 0
average_list = []
while True:
    params = {"area": "1",
              "text": "Python",
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
            average = (salary_from + salary_to) / 2
            average_list.append(average)
            processed_count += 1
        if not salary_from:
            to_rate = salary_to * 0.8
        if not salary_to:
            from_rate = salary_from * 1.2
        sum = 0
        for element in average_list:
            sum += element
        average_salary = sum / len(average_list)
    salary_info_dict["Python"] = {"vacancies_found": total_number,
                                  "vacancies_processed": processed_count,
                                  "average_salary": int(average_salary)
                                  }
print(salary_info_dict)
