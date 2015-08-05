import requests
from bs4 import BeautifulSoup
from app import create_app
import datetime
from flask import current_app
from flask_mail import Mail, Message

app = create_app ('config')
mail = Mail(app)
msg = Message("Failed to add sites",
                  sender="leo@search.techarena51.com",
                  recipients=["leo.gonzalvez@gmail.com"])

headers = { 'user-agent': 'testing:v0.1 (by /u/12boy)' }

site = requests.get("https://news.ycombinator.com/", headers=headers)

soup = BeautifulSoup(site.text, 'html.parser')

for div in soup.find_all(class_="athing"):
       #Ad links have no score on ycombinate eg: search for Zesty
      if div.contents[4].a != None and div.next_sibling.span != None:
          url = div.contents[4].a.get('href')
          tag = div.contents[4].a.get_text()
          ycombinator_score, string = div.next_sibling.span.get_text().split()
          content = ""

      with app.app_context():
             from app.sites.models import Sites
             site=Sites(url, content, tag, ycombinator_score=ycombinator_score)
             error = site.add(site)
             if error != None:
                msg.body =""" URL : {url},
                              tag: {tag},
                              score:{score},
                              html : {div},
                              ERROR = {error}""".format(url=url,
                                                      tag=tag,
                                                      score=ycombinator_score,
                                                      div=div,
                                                      error=error)
                #mail.send(msg)
                print(error)
                continue
