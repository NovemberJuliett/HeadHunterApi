import requests
from pprint import pprint

languages_list = ["JavaScript", "Java", "Python", "PHP", "C++", "C#", "C", "Go", "Shell"]
base_url = 'https://api.hh.ru/vacancies'


languages_dict = {}
for language in languages_list:
    link = f"{base_url}?area=1&text={language}"
    response = requests.get(link)
    count = response.json()["found"]
    languages_dict[language] = count
print(languages_dict)














