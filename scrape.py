from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data import Game

#Scrape results from 2021-2022 regular season

#NEXT STEPS:
#1) Add Date info to each Game object
#2) Traverse each page of each season


#Configure webdriver 
print("Configuring webdriver...")
options= Options()
options.headless= True  # hide GUI
driver= webdriver.Chrome(options=options)
print("Configured webdriver...")
#^consider efficiency improvements 
#e.g. add options for not loading images     


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
		scrapeGame(row)
	return rows


# Given a table row (which corresponds to an NBA game), 
# this function returns a list [homeGame,awayGame], where 
# 'homeGame' and 'awayGame' are Game objects corresponding to
# each game: one object from the perspective of the Home team,
# and one from the perspective of the Away team).
# !Currently doesn't record the date of the game yet!
def scrapeGame(row):
	#initialize the 2 Game objectes
	homeGame= Game()
	awayGame= Game()

	#set the team names
	teams= row.find("td", "table-participant").find('a')
	teamString= teams.text
	homeTeam,awayTeam= teamString.split(' - ')
	homeGame.team= homeTeam
	awayGame.team= awayTeam

	#set the winner/loser
	winner= teams.find("span","bold").text
	homeGame.outcome= int(winner==homeTeam)
	awayGame.outcome= int(winner==awayTeam)

	#set the odds
	odds= row.find_all("td","odds-nowrp")
	homeWinOdds,awayWinOdds= [odd.text for odd in odds]
	homeGame.winOdds= homeWinOdds
	awayGame.winOdds= awayWinOdds
	homeGame.loseOdds= awayWinOdds 
	awayGame.loseOdds= homeWinOdds

	print("Home game:")
	print(homeGame)
	print("\nAway game:")
	print(awayGame)
	print("\n\n\n\n")

	return [homeGame, awayGame]





if __name__ == '__main__':
	
	url= "https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/3/"

	print("Making soup...")
	soup= makeSoup(url)
	print("Made soup")

	print("Getting table data...")
	games= getAllGameData(soup)
	#print(games)

	driver.quit()