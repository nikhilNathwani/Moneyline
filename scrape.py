from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Scrape results from 2021-2022 regular season
#Output should be a list of dicts containing: 
#	"team": <team name (str)>
#   "date": <date of game (datetime)>
#   "outcome": <1 if team won, 0 if lost (int/bool)>
#   "odds": <moneyline (int)> 


#Configure webdriver 
print("Configuring webdriver...")
options= Options()
options.headless= True  # hide GUI
driver= webdriver.Chrome(options=options)
print("Configured webdriver...")
#^consider efficiency improvements e.g. add options for not loading images     


def makeSoup(url):
	#Get page contents
	driver.get(url)
	html= driver.page_source
	return BeautifulSoup(html,'lxml')


#Leaving date aside for now
def getAllGameData(soup):
	table= soup.find("table", "table-main")
	rows= table.find_all("tr", class_="deactivate")
	for row in rows: 
		print(row.prettify())
		print("\n\n\n")
		scrapeGame(row)
	return rows


#Given a table row (which corresponds to an NBA game), 
#this function returns a list [a,b], where 'a' and 'b' 
#are game dicts for the 2 teams that played in that game.
#!Currently doesn't record the date of the game yet!
def scrapeGame(row):
	teams= row.find("td", "table-participant")







if __name__ == '__main__':
	print("Making soup...")
	soup= makeSoup("https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/3/")
	print("Made soup")

	print("Getting table data...")
	games= getGameData(soup)
	#print(games)

	driver.quit()