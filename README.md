# tinder_bot
Uses machine learning to swipe right on the QTs and left on the not QTs.

# Usage
```
python -i main.py
bot = TinderBot()
```
Then chrome should pop up. Log into your tinder account.
Exit the browser and rerun the program. It then should start swiping


# Issues
If you run into issues running the first time through. The reason
may because orignally I logged in every time instead of using cookies/local storage.
I then didnt update my code too much so I had a few extra files like privateinfo.py.
You also may have to remove the line 
```
from privateinfo.py import *
```
its like line 29.
Then in the constructor of TinderBot, remove line 210 self.login().
Then the usage becomes:
```
python -i main.py
bot = TinderBot()
```
Wait til you log in and then type
```
bot.swipeStage()
```
