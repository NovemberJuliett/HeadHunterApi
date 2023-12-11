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
print(languages_dict)


params = {"area": "1",
          "text": "Python"}
response = requests.get(base_url, params=params)
vacancy_features = response.json()["items"]
for feature in vacancy_features:
    salary = feature["salary"]
    print(salary)















