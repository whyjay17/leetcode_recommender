import requests
from bs4 import BeautifulSoup as bs

# Import TfIdfVectorizer from scikit-learn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# The pages does a POST request for dynamic content. Need to send a MySql query to database

question_name = 'two-sum'

data = {"operationName":"questionData","variables":{"titleSlug":"{}".format(question_name)},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

r = requests.post('https://leetcode.com/graphql', json = data).json()
soup = bs(r['data']['question']['content'], 'lxml')
title = r['data']['question']['title'] # question name
content =  soup.get_text().replace('\n',' ') # question content

tokens = content.split(' ')
stop_words = set(stopwords.words('english')) 
filtered_sentence = [w for w in tokens if not w in stop_words and w.isalpha()] 
print(filtered_sentence)