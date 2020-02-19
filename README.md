# tinder_bot
Uses machine learning to swipe right on the QTs and left on the not QTs.

# Usage
```
python3 main.py
```
Then chrome should pop up. Log into your tinder account.
Exit the browser and rerun the program. It then should start swiping

# NOTE
If you do/dont want to save any images for further ml than change the last 
few lines in main.py from

if you want to save
```
bot.startSwiping(willSave=True)
```
you dont want to save
```
bot.startSwiping(willSave=False)
```
to

