import requests
import json
import csv
from bs4 import BeautifulSoup as bs
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 

# request question list from the api
req = requests.get(url='https://leetcode.com/api/problems/algorithms/')

# get json data
json_data = json.loads(req.text)

# get question list 
questions = json_data['stat_status_pairs']

# stop words
stop_words = set(stopwords.words('english')) 

with open('leetcode_data_processed_topics.csv', 'w', newline='', encoding='UTF-8') as csvfile:
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
            soup = bs(r['data']['question']['content'], 'html')
            title = r['data']['question']['title'] # question name
            topics = r['data']['question']['topicTags'] # get topic list
            # print('Question = {}, topics = {}'.format(title, [item['name'] for item in topic_arr]))
            topic_arr = [item['name'].lower() for item in topics]
            content =  soup.get_text().replace('\n',' ') # question content
            tokens = content.split(' ')
            filtered_sentence = [w.lower() for w in tokens if not w in stop_words and w.isalpha() and w != 'Example']
            writer.writerow([stat['question_id'], title, filtered_sentence + topic_arr, difficulty])
        
