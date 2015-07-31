import requests
from bs4 import BeautifulSoup
import re

#headers = { 'user-agent': 'testing:v0.1 (by /u/12boy)' }
#site = requests.get("http://www.reddit.com/r/python" ,headers=headers)

soup = BeautifulSoup(open("html-test.html"), 'html.parser')

#print (site.text)

for tag in soup.find_all('div', class_=re.compile('thing')):
        score = ""
        for score in tag.find_all('div', {"class": "score unvoted"}):      
                         print(score.get_text())
                         print("next")
        
        for site in tag.find_all('a', {"class": "title may-blank "}): 
               print(site.get('href'))
               
              
        
        
        
        