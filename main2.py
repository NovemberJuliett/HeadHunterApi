import requests

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]

page = 0
per_page = 100

base_url = "https://api.hh.ru/vacancies"

total_number = 0
while True:
    params = {"area": "1",
              "text": "Python",
              "page": page,
              "per_page": 100}
    language_response = requests.get(base_url, params=params)
    print(language_response.status_code)
    if language_response.status_code != 200:
        print(language_response.json())
        continue
    vacancies = language_response.json()
    print(vacancies)
    list_vacancies = vacancies["items"]
    number_of_vacancies = len(list_vacancies)
    if number_of_vacancies == 0:
        break
    total_number = total_number + number_of_vacancies
    page += 1
    print(total_number)
print(total_number)