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


site = requests.get("https://news.ycombinator.com/")

soup = BeautifulSoup(site.text, 'html.parser')

for tag in soup.find_all(class_="title"):
    if tag.a != None:
        url = tag.a.get('href')
        tag  =  tag.a.get_text()
        content = "news.ycombintator.com, date: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with app.app_context():
             from app.sites.models import Sites     
             site=Sites(url, content, tag)
             error = site.add(site)
             if error != None:
                mail.send(msg)
                break
             
              
             
    



