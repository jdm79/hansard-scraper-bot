import requests
from requests import get
from datetime import date
from bs4 import BeautifulSoup
import datetime
import pandas as pd 
import numpy as np 
import tweepy
import random
import time
import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today = date.today().isoweekday() - 1
day = days[today]
  
headers = {"Accept-language": "en-US, en;q=0.5"}
url = "https://hansard.parliament.uk/lords/"
time_stamp = datetime.datetime.now()
date_stamp = time_stamp.strftime("%Y-%m-%d")

def scrape():
  results = requests.get(url + date_stamp, headers=headers)

  soup = BeautifulSoup(results.text, "html.parser")
  issues_div = soup.find_all('li', class_='no-children')
  issues = []
  nada = "Nothing to report so far today."
  # html_message = soup.find('p')
  # message_string = html_message.text.strip()
  # messages = message_string.split(".")
  
  # if (messages[0].find(".") == -1):
  #   # print(messages[0])
  #   api.update_status(messages[0])
  # else:
  for container in issues_div:
    issue = container.a.text
    issues.append(issue.strip())

  string = ', '.join(sorted(issues))
  intro = day + ", the Lords discussed: "
  cont = "Cont'd... "

  # print(messages[0])

# this needs to be improved:
# clean up the split strings - don't split any words
# deal with larger strings - ones that need three tweets or more 
  if len(string) > 0:
    if len(string) < 250:
      api.update_status(intro + string)
      print(intro + string)
    else:
      first, second = string[:len(string)//2], string[len(string)//2:]
      api.update_status(intro + first)
      print(intro + first)
      time.sleep(5)
      api.update_status(cont + second)
      print(cont + second)
  else:
    api.update_status(nada)
    print(nada)

# Only scrapes Mon-Thurs, as Lords don't sit on Fri, Sat and Sun
if today < 5:
  scrape()
else:
  print("The Lords do not debate on " + day + "s.")
  api.update_status("The Lords do not debate on " + day + "s.")
