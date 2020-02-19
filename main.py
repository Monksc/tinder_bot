"""
MIT License

Copyright (c) 2020 Monksc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from selenium import webdriver
import time
import json
import random
#from privateinfo import *
import coremltools
import PIL.Image
import os

def getRandomString():
    s = ""
    for i in range(20):
        s += random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")
    return s

model = coremltools.models.MLModel('/Users/cameronmonks/Projects/Python/tinder_bot/ml/version3.mlmodel')
def getResults(img):
    global model
    result = model.predict({'image': img})
    return result
def getPredictions(img):
    r = getResults(img)
    yes = r['classLabelProbs']['yes']
    no  = r['classLabelProbs']['no']
    return yes, no
def shouldSwipeRight(element):

    element.screenshot("data/temp.png")
    img = PIL.Image.open("data/temp.png")
    yes, no = getPredictions(img)
    
    if yes > no:
        isYes = True
        percent = yes / (yes + no)
        confident = percent > 0.8 and yes > 0.2
    else:
        isYes = False 
        percent = no / (yes + no)
        confident = percent > 0.8 and no > 0.2

    print(isYes, percent)
    return isYes, confident, yes, no, percent, "data/temp.png"
    

class TinderBot:

    def getElementXPath(self, xpath, count=180):
        while True:
            try:
                 element = self.driver.find_element_by_xpath(xpath)
                 return element
            except:
                count -= 1
                if count == 0:
                    return None
                time.sleep(1)


    def login(self):
        login_btn = self.getElementXPath('/html/body/div[2]/div/div/div/div/div[3]/div[1]/button', count=3)
        
        if login_btn == None:
            #self.swipeStage()
            return


        # havnt really solved loggin in yet
        login_btn.click()

        phoneNumberTXTField = self.getElementXPath('/html/body/div[2]/div/div/div[2]/div[2]/div/input')
        phoneNumberTXTField.send_keys(phoneNumber)

    def swipeLeft(self):
        swipe_left_btn =  self.getElementXPath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]', count=3)
        swipe_left_btn.click()
        self.swipeLeftCount += 1

    def swipeRight(self):
        swipe_right_btn = self.getElementXPath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]', count=3)
        swipe_right_btn.click()
        self.swipeRightCount += 1

    def flipThroughImages(self):

        i = 1
        while True:
            element_id = '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/button[' + str(i) + ']'
            element = self.getElementXPath(element_id, count=(5 if i == 0 else 1))

            if element == None:
                break
            
            element.click()
            time.sleep(0.25)
            yield self.getElementXPath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]', count=1)

            i += 1

    def collectDataYes(self):
        
        for element in self.flipThroughImages():
            filename = "data/camswipe/yes/" + getRandomString() + ".png"
            element.screenshot(filename=filename)

        self.swipeRight()

    def collectDataNo(self):

        for element in self.flipThroughImages():
            filename = "data/camswipe/no/" + getRandomString() + ".png"
            element.screenshot(filename=filename)

        self.swipeLeft()

    def startSwiping(self, willSave=False):

        self.swipeRightCount = 0
        self.swipeLeftCount = 0

        while True:
            self.swipeAndSave(willSave)


    def swipeAndSave(self, willSave):

        totalYes = 0
        totalNo = 0
        yesConfident = 0
        noConfident = 0

        for element in self.flipThroughImages():
            
            isSwipeRight, isConfident, yes, no, percent, filename = shouldSwipeRight(element)
            print(isSwipeRight, percent)

            totalYes += yes
            totalNo += no

            if isConfident:
                if isSwipeRight:
                    yesConfident += 1
                else:
                    noConfident += 1


            if willSave:
                if isSwipeRight:
                    newFilename = "data/botswipe/yes/" + str(percent) + "00000" + getRandomString() + ".png"
                    os.rename(filename, newFilename)
                    #element.screenshot(filename=filename)
                else:
                    newFilename = "data/botswipe/no/" + str(percent) + "00000" + getRandomString() + ".png"
                    os.rename(filename, newFilename)
                    #element.screenshot(filename=filename)

        print("TOTAL YES:", totalYes, " TOTAL NO:", totalNo, " yesConfident:", yesConfident, " noConfident:", noConfident)
        if totalYes > totalNo and yesConfident > noConfident:
            self.swipeRight()
        else:
            self.swipeLeft()

        print("RIGHT: ", self.swipeRightCount, " LEFT: ", self.swipeLeftCount, " PERCENT: ", (self.swipeRightCount / (self.swipeRightCount + self.swipeLeftCount)))



    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=selenium")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://tinder.com")

        with open('cookies.json') as json_file:
            data = json.load(json_file)
            for cookie in data:
                self.driver.add_cookie(cookie)

        with open('localStorage.json') as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                self.driver.execute_script("localStorage.setItem('" + key + "', '" + value + "')")

if __name__ == "__main__":
    bot = TinderBot()
    time.sleep(10)
    bot.startSwiping(willSave=False)
