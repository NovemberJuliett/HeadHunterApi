import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
token = os.environ["SUPERJOB_TOKEN"]
url = "https://api.superjob.ru/2.0/vacancies"

headers = {"X-Api-App-Id": token}
params = {
    "town": 4,
    "catalogues": 33}
response = requests.get(url, headers=headers, params=params)
data = response.json()
pprint(data)

