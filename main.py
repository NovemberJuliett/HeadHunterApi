import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
token = os.environ["SUPERJOB_TOKEN"]
url = "https://api.superjob.ru/2.0/vacancies"

headers = {"X-Api-App-Id": token}
params = {
    "town": {
        'declension': 'в Москве',
                       'genitive': 'Москвы',
                       'hasMetro': True,
                       'id': 4,
                       'title': 'Москва',
    },
    "catalogues": {"title_rus":"Разработка, программирование",
                   "url_rus":"razrabotka-po",
                   "title":"Разработка, программирование",
                   "id_parent":33,
                   "key":48}
}
response = requests.get(url, headers=headers, params=params)
data = response.json()
pprint(data)

