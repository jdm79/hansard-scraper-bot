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

# on the private live repo version of this, the auth tokens are placed here because Heroku
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
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
  
  # this gets rid of the span texts (item number n) etc
  for span_tag in soup.findAll('span'):
    span_tag.replace_with('')

  # they changed it...
  issues_div = soup.find_all('div', class_='primary-info')
  issues_list = []
  nada = "Nothing to report so far today."

  for container in issues_div:
    issue = container.text
    issues_list.append(issue.strip())

  # make the items in the list unique
  issues_set = set(issues_list)

  # convert back to list
  issues = list(issues_set)

  string_dirty = ', '.join(sorted(issues))
  string = string_dirty.replace('Arrangement of Business', '')
  string = string.replace('Regulations 2020', 'Regs 2020')
  string = string.replace('Business of the House', 'BoH')
  string = string.replace('House of Lords', 'HoL')
  string = string.replace('Lord Speaker’s Statement', 'LSS')
  string = string.replace('Whole day', '|')
  string = string[2:]

  intro = day + ", the Lords discussed: "
  cont = "Cont'd: "
  pdf_link = "https://hansard.parliament.uk/pdf/lords/" + date_stamp
  pdf_tweet = "You can download the Hansard record of the entire day in PDF format here: " + pdf_link

  if len(string) < 242:
    api.update_status(intro + string)
    api.update_status(pdf_tweet)

  elif len(string) < 500:
    first, second = string[:len(string)//2], string[len(string)//2:]
    api.update_status(intro + first)
    api.update_status(cont + second)
    api.update_status(pdf_tweet)

  elif len(string) < 774:
    first = string[:242]
    second = string[242:508]
    third = string[508:774]
    api.update_status(intro + first + " (1/3)")
    api.update_status(cont + second + " (2/3)")
    api.update_status(cont + third + " (3/3)")
    api.update_status(pdf_tweet)

  elif len(string) < 1040:
    first = string[:242]
    second = string[242:508]
    third = string[508:774]
    fourth = string[774:1040]

    api.update_status(intro + first + " (1/4)")
    api.update_status(cont + second + " (2/4)")
    api.update_status(cont + third + " (3/4)")
    api.update_status(cont + fourth + " (4/4)")
    api.update_status(pdf_tweet)

  elif len(string) < 1306:
    first = string[:242]
    second = string[242:508]
    third = string[508:774]
    fourth = string[774:1040] 
    fifth = string[1040:1306]

    api.update_status(intro + first + " (1/5)")
    api.update_status(cont + second + " (2/5)")
    api.update_status(cont + third + " (3/5)")
    api.update_status(cont + fourth + " (4/5)")
    if len(fifth) > 0: 
      api.update_status(cont + fifth + " (5/5)")
    api.update_status(pdf_tweet)

  elif len(string) < 1572:
    first = string[:242]
    second = string[242:508]
    third = string[508:774]
    fourth = string[774:1040] 
    fifth = string[1040:1306]
    sixth = string[1306:1572]

    api.update_status(intro + first + " (1/6)")
    api.update_status(cont + second + " (2/6)")
    api.update_status(cont + third + " (3/6)")
    api.update_status(cont + fourth + " (4/6)")
    api.update_status(cont + fifth + " (5/6)")
    if len(sixth) > 0:
      api.update_status(cont + sixth + " (6/6)")
    api.update_status(pdf_tweet)

  else:
    api.update_status(nada)

if today < 4:
  scrape()
else:
  api.update_status("The Lords do not debate on " + day + "s.")
