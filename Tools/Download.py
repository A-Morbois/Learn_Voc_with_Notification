#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import codecs
import io
import urllib


OutPath = "/home/antoine/Bureau/Learn_Voc_Notification/Sound"
profile = webdriver.FirefoxProfile()

#Force the download without having the pop up
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.alwaysAsk.force", "false");
profile.set_preference("browser.download.manager.showWhenStarting","false");
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", OutPath)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream"+",application/zip"+",application/x-rar-compressed"+",application/x-gzip"+",application/msword"+",audio/mpeg"+",audio/x-ms-wma"+",audio/vnd.rn-realaudio"   +",audio/x-wav")
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/firefox"
binary = FirefoxBinary('/usr/bin/firefox')

driver =  webdriver.Firefox(profile)
driver.get('https://google.com/')

#Foreach line containing some vocabulary
with io.open("30_Step.txt", encoding ="utf-8") as f:
    for line in f:
        words = line.split(";")

        ## Images
        print " Processing word : " + words[0]
        url = 'https://pixabay.com/zh/'
        driver.get(url)

        # Go in Sound Of Text to download the sound
        text_area = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div/span/input')
        query = words[0]
        text_area.send_keys(query)
        #text_area.sendKeys(Keys.RETURN)

        search = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div/input')
        search.click()

        img = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]/a/img')
        src = img.get_attribute('src')
        urllib.urlretrieve(src,words[0] +".jpg")

        time.sleep(2)

        ## Sound
        driver.get('https://soundoftext.com/')

        # Go in Sound Of Text to download the sound
        text_area = driver.find_element_by_name('text')
        text_area.send_keys(query)

        voice = driver.find_element_by_xpath('/html/body/div[1]/div/main/section[1]/div[1]/div/form/div[2]/select')
        voice.click()
        voice.send_keys("Cc") # Chinese in the list
        voice.click()

        submit_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/section[1]/div[1]/div/form/div[3]/input')
        submit_button.click()

        # Give the page some time to load its resources
        time.sleep(5)
        download = driver.find_element_by_xpath('/html/body/div[1]/div/main/section[1]/div[2]/div/div/div[2]/a[2]')
        download.click()

        time.sleep(2)
