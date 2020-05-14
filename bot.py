import requests
from requests import get
from datetime import date
from bs4 import BeautifulSoup
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
  issues_list = []
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
    issues_list.append(issue.strip())

  # make the items in the list unique
  issues_set = set(issues_list)
  issues_set.remove("House of Lords")

  # convert back to list
  issues = list(issues_set)

  string = ', '.join(sorted(issues))

  intro = day + ", the Lords discussed: "
  cont = "Cont'd... "

  if len(string) > 0:
    if len(string) < 250:
      api.update_status(intro + string)
    else:
      first, second = string[:len(string)//2], string[len(string)//2:]
      if len(first) < 280:
        api.update_status(intro + first)
        api.update_status(cont + second)
      else:
        first_frag, second_frag = first[:len(first)//2], first[len(first)//2:]
        third_frag, fourth_frag = second[:len(second)//2], second[len(second)//2:]

        time.sleep(3)

        print(second_frag)
        api.update_status(intro + first_frag)
        api.update_status(cont + second_frag)

        time.sleep(3)

        api.update_status(cont + third_frag)
        api.update_status(cont + fourth_frag)
  else:
    api.update_status(nada)

if today < 4:
  scrape()
else:
  api.update_status("The Lords do not debate on " + day + "s.")
