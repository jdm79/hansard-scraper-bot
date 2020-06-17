## Python web scraper Twitter bot

This script scrapes the [House of Lords Hansard website](https://hansard.parliament.uk/lords/) every day at 6pm and tweets the issues debated that day (if they are debating - which they don't usually do on Fri, Sat and Sun). 

This is not the github repo for the Twitter bot now that it's on Heroku as I don't want to have my API tokens and oauth in public. Currently I keep the tokens and oauth stuff all in the same main file now, as the config wasn't working on Heroku. Whenever I update the private repo, I try to keep this repo similar.

In the other repo I have another script similar to this which runs at 10pm as the final round-up - it is usually different too as they seem to never stop updating these lists. 

It runs on a free Heroku account using the Heroku Scheduler add-on for both scripts. I wrote this script originally in Ruby and ran it on my local machine on a 24-hour loop.

I've put this up here as much for my future self, to remind me how this all works and to use as a template. 

You can visit this bot on Twitter [here](https://twitter.com/HansardLord).

### Features

This is very basic right now, as it was made very quickly. The list on the Hansard website is revised throughout the day, but usually the final list is up by 6pm, which is when this bot is scheduled to scrape.

Sometimes the issues listed on Hansard create a string longer than 280 characters, so I've added some conditionals to deal with this, to chop up the string and tweet in chunks - otherwise Tweepy just won't tweet anything if the string is too long. I'm chopping the string in half and tweeting the first half, then checking again to see it fits, and so on. This means words will be chopped up sometimes. I might get around to refactoring this.

### How to use (I'm assuming some knowledge of git, but definitely worth looking at Heroku docs too - they are much easier than AWS Lambda)

1. Git clone this repo
2. Apply for a Twitter developer account, stick your tokens and keys in config.py
3. Create your own requirements.txt by typing the following:

  ```
    $ pip3 freeze > requirements.txt
  ```
or:

  ```
    $ pip3 install <whichever other Python libraries you want>
  ```
4. Do your Heroku create stuff after you've git init, added and committed, git push heroku master it to the cloud and add the heroku scheduler add-on, set the schedule to whenever you want it and use the following script command: 
  ```
    $ python bot.py
  ```

If you're scraping a different website, you'll have to use inspect element on the html page to find the elements you want and change the code accordingly.

