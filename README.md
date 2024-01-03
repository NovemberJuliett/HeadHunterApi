# Programming vacancies compare

This script helps to compare developers salaries on HeadHunter and SuperJob sites,
based on programming language.

## How to install

Python3 should be already installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
## How to use

Firstly you should receive API key for using SuperJob API following the instruction
[on this site](https://api.superjob.ru/?from_refresh=1). You don't need API key for using HeadHunter API.

Then you should create .env file in your project directory
(or in the root of your project).

Create new variable in the same .env file and put your service key here. For example:

```python 
SUPERJOB_API_KEY ="put_your_api_key_here"
```

## Run

Open a new terminal window and run the script:
```python
python main.py
```