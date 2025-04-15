import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys

class CSVEntry:
    def __init__(self, emails, channelname, subscribercount=0):
        self.emails = emails
        self.channelname = channelname
        self.subscribercount = subscribercount
    def toCSV(self, searchsubject,outputfile = 0):
        output = ""
        print self.emails
        if len(self.emails) >= 1:
            for email in self.emails:
                output = output + email.encode('utf-8', 'ignore') + ','
        output = output + self.channelname.encode('utf-8', 'ignore') + ','
        output = output + self.subscribercount.encode('utf-8', 'ignore')
        output = output + '\n'
        
        if outputfile == 0:
            return output     
        else:
            if not os.path.isfile(outputfile):
                try:
                    with open(outputfile, 'w+') as f:
                        f.write("Search Subject:," + searchsubject + ", Amount of days before today searched:," + str(daysinthepast) + "\n")
                        f.write("Email Addresses in description, Channel Name, Subscriber Count\n")
                        f.close()
                except Exception,e:
                    print "Exception! Error writing to output file."
                    print type(e)
                    print str(e)
                    a = raw_input(" ")
            with open(outputfile, 'a+') as f:
                f.write(output)
                f.close()
            return
def StartupTest(driver):
    try:
        driver.get("http://www.youtube.com")
    except:
        time.sleep(1)
        StartupTest(driver)
    return driver

def main(SearchTerm):
    APIKEY = "XXXXXXXXXXXXXXX"  
    print SearchTerm
    driver = webdriver.Firefox()
    driver = StartupTest(driver)
    driver = NavigateToYoutubeAndSearch(driver, SearchTerm)
    BeginSearchParsing(driver)
    
def NavigateToYoutubeAndSearch(driver, searchterm):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "masthead-search-term"))
        )
    except:
        print "Waiting..."
        time.sleep(5)
        element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "masthead-search-term"))
            )
    
    
    print "Finding Search box..."
    SearchBox= driver.find_element_by_id("masthead-search-terms")
    print SearchBox  
    SearchButton = driver.find_element_by_id("search-btn")
    SearchBox.send_keys(searchterm)
    SearchButton.click()
    return driver

def BeginSearchParsing(driver):
    emailregexpattern = r'(\w(?:[-.+]?\w+)+\@(?:[a-zA-Z0-9](?:[-+]?\w+)*\.)+[a-zA-Z]{2,})'
    p = re.compile(emailregexpattern)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[1]/div/div[1]/div/p"))
        )
    finally:
        driver.quit()
    ResultCount = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[1]/div/div[1]/div/p")
    ResultNumber = ResultCount.text
    print ResultNumber   
    while True:
        PageofSearchResults = driver.find_elements_by_class_name("item-section")
        Videos = PageofSearchResults[0].find_elements_by_xpath("/html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[2]/ol/li/div")
        for video in Videos:
            description = video.find_element_by_xpath("/html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[2]/ol/li[4]/div/div/div[2]/div[3]")
            if "@" in desc.text:
                if bool(p.search(line)) == True:
                    emails = re.findall(emailregexpattern, description)
                    outputpath = os.path.expanduser("~")
                    nowtime = time.strftime("%m-%d-%Y")
                    filename = "youtubeoutput " + nowtime + "_" + searchsubject +  ".csv"
                    outputfullpath = os.path.join(outputpath, filename)
                    entry.toCSV(searchsubject, outputfullpath)
            else:
                continue
        Buttons = driver.find_elements_by_class_name("yt-uix-button-content")
        for button in Buttons:
            if "Next" in button.text:
                NextButton = button
                button.click()
    try:
        driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
    finally:
        print "Error finding page."
        driver.quit()

