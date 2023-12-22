import requests
from pprint import pprint

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = "https://api.hh.ru/vacancies"


def predict_rub_salary(url):
    average_list = []
    processed_count = 0
    response = requests.get(url)
    vacancy_features = response.json()["items"]
    for feature in vacancy_features:
        salary = feature["salary"]
        if not salary:
            continue
        salary_from = salary["from"]
        salary_to = salary["to"]
        if salary_from and salary_to:
            average = (salary_from + salary_to) / 2
            average_list.append(average)
            processed_count += 1
        else:
            if not salary_from:
                to_rate = salary_to * 0.8
            if not salary_to:
                from_rate = salary_from * 1.2
    sum = 0
    for element in average_list:
        sum += element
    average_salary = sum/len(average_list)
    return processed_count, int(average_salary)


# salary_info_dict = {}
# for language in languages_list:
#     params = {"area": "1",
#               "text": f"{language}"}
#     language_response = requests.get(base_url, params=params)
#     vacancy = language_response.url
#     count = language_response.json()
#     vacancy_number, average_salary = predict_rub_salary(vacancy)
#     salary_info_dict[language] = {"vacancies_found": count["found"],
#                                   "vacancies_processed": vacancy_number,
#                                   "average_salary": average_salary}
# print(salary_info_dict)


def get_all_vacancies():
    page = 0
    per_page = 100
    all_vacancies = []
    salary_info_dict = {}

    while True:
        for language in languages_list:
            params = {"area": "1",
                      "text": f"{language}",
                      "page": page,
                      "per_page": per_page
                      }
            language_response = requests.get(base_url, params=params)
            vacancies_data = language_response.json()
            all_vacancies.extend(vacancies_data["items"])
            page += 1
        return salary_info_dict

pprint(get_all_vacancies())