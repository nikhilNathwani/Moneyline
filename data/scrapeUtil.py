#Functions that aid in the scraping of oddsportal.com

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#Configure webdriver 
options= Options()
#options.headless= True  # hide GUI
driver= webdriver.Chrome(options=options)
#^consider efficiency improvements 
#e.g. add options for not loading images     

waitTime= 3 #seconds

def makeSoup(url):
	#Get page contents
	driver.get(url)
	time.sleep(waitTime)
	html= driver.page_source
	time.sleep(waitTime)
	return BeautifulSoup(html,'lxml')

def endScrape():
	driver.quit()

def isHeaderRow(row):
	return 'nob-border' in row.get("class")

def isPlayoffs(row):
	header= row.find('th')
	return header.text.split(' - ')[-1] == "Play Offs"

def isPreSeason(row):
	header= row.find('th')
	return header.text.split(' - ')[-1] == "Pre-season"

#2020 season had a mid-season "pre-season" before the bubble began
#need to ignore these "pre-season" but only when the year is 2020
def is2020(row):
	header= row.find('th')
	return header.text.split(' - ')[0].split(' ')[-1] == "2020"	

def isAllStarGame(row):
	header= row.find('th')
	return header.text.split(' - ')[-1] == "All Stars"

def isRegularSeason(row):
	return not isPlayoffs(row) and not isPreSeason(row) and not isAllStarGame(row)