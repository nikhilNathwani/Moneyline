from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Configure webdriver 
print("Configuring webdriver...")
options= Options()
options.headless= True  # hide GUI
driver= webdriver.Chrome(options=options)
print("Configured webdriver...")
#^consider efficiency improvements e.g. add options for not loading images     


#Scrape results from 2021-2022 regular season
#Output should be a list of dicts containing: 
#	"team": <team name (str)>
#   "date": <date of game (datetime)>
#   "outcome": <1 if team won, 0 if lost (int/bool)>
#   "odds": <moneyline (int)>   


def makeSoup(url):
	#Get page contents
	driver.get(url)
	html= driver.page_source
	return BeautifulSoup(html,'lxml')

def getGameData(soup):
	table= soup.find("table", "table-main")
	rows= table.find_all("tr", class_="deactivate")
	return rows

if __name__ == '__main__':
	print("Making soup...")
	soup= makeSoup("https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/3/")
	print("Made soup")

	print("Getting table data...")
	games= getGameData(soup)
	print(games)

	driver.quit()