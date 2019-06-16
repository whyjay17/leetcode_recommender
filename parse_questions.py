import requests
import json
import csv
from bs4 import BeautifulSoup as bs

# request question list from the api
req = requests.get(url='https://leetcode.com/api/problems/algorithms/')

# get json data
json_data = json.loads(req.text)

# get question list 
questions = json_data['stat_status_pairs']

with open('leetcode_data.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    existing_accounts = []
    
    # header
    writer.writerow(["id", "name", "content", "difficulty"])
    
    for json in questions:
        # get the meta info of algorithm
        stat = json['stat']
        difficulty = json['difficulty']['level']
        question_name = stat['question__title_slug'] 
        # print(question_name)

        # The pages does a POST request for dynamic content. Need to send a MySql query to database
        data = {"operationName":"questionData","variables":{"titleSlug":"{}".format(question_name)},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

        r = requests.post('https://leetcode.com/graphql', json = data).json()

        if r['data']['question']['content']:
            soup = bs(r['data']['question']['content'], 'lxml')
            title = r['data']['question']['title'] # question name
            content =  soup.get_text().replace('\n',' ') # question content

            writer.writerow([stat['question_id'], title, content, difficulty])
        
