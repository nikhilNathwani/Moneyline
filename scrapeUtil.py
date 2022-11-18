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

def makeSoup(url):
	#Get page contents
	driver.get(url)
	time.sleep(3)
	html= driver.page_source
	time.sleep(3)
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

def isAllStarGame(row):
	header= row.find('th')
	return header.text.split(' - ')[-1] == "All Stars"

def isRegularSeason(row):
	return not isPlayoffs(row) and not isPreSeason(row) and not isAllStarGame(row)