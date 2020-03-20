## Python web scraper Twitter bot

This script scrapes the [House of Lords Hansard website](https://hansard.parliament.uk/lords/) every day at 6pm and tweets the issues debated that day (if they are debating - which they don't usually do on Fri, Sat and Sun).

It runs on a free Heroku account using the Heroku Scheduler add-on. I wrote this script originally in Ruby and ran it on my local machine on a 24-hour loop.

I've put this up here as much for my future self, to remind me how this all works and to use as a template. 

You can visit me on Twitter [here](https://twitter.com/HansardLord).

### Features

This is very crude and basic. The list is revised throughout the day. Usually by 6pm the list is up, but not always the final list.

Sometimes the issues listed on Hansard create a string longer than 280 characters, so I've added some conditionals to deal with this, to chop up the string and tweet in chunks - otherwise Tweepy just won't tweet anything if the string is too long. I'm chopping the string in half and tweeting the first half, then checking again to see it fits, and so on. This means words will be chopped up sometimes. I might get around to refactoring this.

### How to use

1. Git clone this repo
2. Apply for a Twitter developer account, stick your tokens and keys in config.py
3. Create your own requirements.txt by typing the following:

  ```
    $ pip3 freeze > requirements.txt
  ```
or:

  ```
    $ pip3 install <whatever other Python libraries you want>
  ```
4. Do your Heroku create stuff, git push heroku master it to the cloud and add the heroku scheduler add-on, set the schedule to whenever you want it and use the following script command: 
  ```
    $ python bot.py
  ```

If you're scraping a different account, you'll have to use inspect element on the html page to find the elements you want and change the code accordingly.

ALWAYS PUT YOUR CONFIG.PY IN .GITIGNORE, else people will see your secret tokens and keys and take over your bots!