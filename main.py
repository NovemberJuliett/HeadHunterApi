import requests
from pprint import pprint

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = "https://api.hh.ru/vacancies"


salary_info_dict = {}


def predict_rub_salary(url):
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
            print(average)
        else:
            if not salary_from:
                to_rate = salary_to * 0.8
                print(to_rate)
            if not salary_to:
                from_rate = salary_from * 1.2
                print(from_rate)
            if salary["currency"] != "RUR":
                print(None)
    for language in languages_list:
        params = {"area": "1",
                  "text": f"{language}"}
        response = requests.get(base_url, params=params)
        vacancy = response.url
        count = response.json()
        salary_info_dict[language] = {"vacancies_found": count["found"]},
                                      # "vacancies_processed": predict_rub_salary(vacancy)

print(salary_info_dict)



# predict_rub_salary("https://api.hh.ru/vacancies?area=1&text=Python")
