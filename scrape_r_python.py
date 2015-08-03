import requests
from bs4 import BeautifulSoup
import re
from flask import current_app
from flask_mail import Mail, Message
from app import create_app

app = create_app ('config')
mail = Mail(app)
msg = Message("Failed to add sites",
                  sender="leo@search.techarena51.com",
                  recipients=["leo.gonzalvez@gmail.com"])
                  

subs = [ "programming", "python", "coding"]

for sub in subs:

    headers = { 'user-agent': 'testing:v0.1 (by /u/12boy)' }
    site = requests.get("http://www.reddit.com/r/{}".format(sub) ,headers=headers)

    soup = BeautifulSoup(site.text, 'html.parser')

    #print (site.text)

    for div in soup.find_all('div', class_=re.compile('thing')):

        try:
            score = int(div.div.contents[2].get_text())
            if score > 10:
                
                url = div.div.next_sibling.a.get('href')
                tag = div.div.next_sibling.a.get_text()
                content = ""
                with app.app_context():
                     from app.sites.models import Sites     
                     site=Sites(url, content, tag, reddit_score=score)
                     error = site.add(site)
                     if error != None:
                        msg.body =" URL : {url}, tag: {tag}, score:{score}, html : {div}, ERROR = {error}".format(url=url,
                                                                                                                  tag=tag,
                                                                                                                  score=score,
                                                                                                                  div=div,
                                                                                                                  error=error
                                                                                                                 )
                        mail.send(msg)
                        continue
        except ValueError:
            continue

