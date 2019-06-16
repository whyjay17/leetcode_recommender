import requests
import json
from bs4 import BeautifulSoup as bs

# request question list from the api
req = requests.get(url='https://leetcode.com/api/problems/algorithms/')

# get json data
json_data = json.loads(req.text)

# get question list 
questions = json_data['stat_status_pairs']

for json in questions:
    # get the meta info of algorithm
    stat = json['stat']
    difficulty = json['difficulty']['level']
    question_name = stat['question__title_slug'] 
    print(question_name)
