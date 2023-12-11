import requests
from pprint import pprint

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = "https://api.hh.ru/vacancies"

languages_dict = {}
for language in languages_list:
    params = {"area": "1",
              "text": f"{language}"}
    response = requests.get(base_url, params=params)
    count = response.json()
    languages_dict[language] = count["found"]


def predict_rub_salary(vacancy):
    response = requests.get(vacancy)
    vacancy_features = response.json()["items"]
    for feature in vacancy_features:
        salary = feature["salary"]
        if not salary:
            print(None)
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


predict_rub_salary("https://api.hh.ru/vacancies?area=1&text=Python")
