from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
import calendar
from data import Game

#Scrape results from 2021-2022 regular season

#Notes:
#1) oddsportal.com takes an average moneyline across many bookers
#2) oddsportal.com seems to have the dates of games all wrong. But
#   this isn't necessarily a deal-breaker. I don't care about the 
#   exact date, I just care about the order of the games. So I'll
#   try to number the game dates from 0 to [num games] for each team. 

#NEXT STEPS:
#1) Add Date info to each Game object <- UPDATE: per Note #2, will
#   just record the number of the game from 0 to [num games]
#2) Traverse each page of each season
#3) Filter out non-regular-season games


#Global variables
teamGames= {}
currentSeasonStartYear= 0

#Configure webdriver 
print("Configuring webdriver...")
options= Options()
#options.headless= True  # hide GUI
driver= webdriver.Chrome(options=options)
print("Configured webdriver...")
#^consider efficiency improvements 
#e.g. add options for not loading images     


def makeSoup(url):
	#Get page contents
	driver.get(url)
	time.sleep(3)
	html= driver.page_source
	time.sleep(3)
	return BeautifulSoup(html,'lxml')

#scrapes NBA seasons from [startYear]-[startYear+1] to [endYear-1]-[endYear]
def scrapeSeasons(startYear,endYear):
	global currentSeasonStartYear
	global teamGames
	allGameObjects= []
	y= startYear
	while y < endYear:
		currentSeasonStartYear= y
		gameObjectsFromSeason= scrapeSeason(y)
		allGameObjects+= gameObjectsFromSeason
		teamGames= {} #so that gameNum counts reset before scraping the next season
		y+= 1
	return allGameObjects

def scrapeSeason(startYear):
	urlBase= "https://www.oddsportal.com/basketball/usa/nba-"
	urlBase+= str(startYear)+"-"+str(startYear+1)+"/results/#/page/"
	pageNum= 1
	doneTraversing= 0
	allGameObjects= []
	while not doneTraversing:
		url= urlBase+str(pageNum)+"/"
		print("SCRAPING PAGE ", pageNum, '\n\n\n\n\n\n')
		isFinalPage,gameObjectsFromPage= getGameDataFromPage(url)
		allGameObjects+= gameObjectsFromPage
		pageNum+= 1
		doneTraversing= isFinalPage
	return allGameObjects


#look through header rows and game rows:
#1) if we're under a playoff header, skip those games
#2) while we're under regular season headers, add those games to gameObjects list
#3) once we hit a preseason header, stop scraping
#Returns tuple (a,b), where:
# - 'a' is a bool that is 1 if this is the final page to scrape, 0 if we need to keep going
# - 'b' is the gameObject list from the given page
def getGameDataFromPage(url):
	soup= makeSoup(url)
	table= soup.find("table", "table-main")
	#game rows have class "deactivate", and header rows have class "nob-border"
	#header rows indicate whether the next games are playoffs/preseason/etc.
	rows= table.find_all_next("tr", {"class":["deactivate", 'nob-border']})
	gameObjects= []
	regularSeason= 0
	finalPage=0 
	for row in rows:
		if isHeaderRow(row):
			regularSeason= isRegularSeason(row)
			if isPreSeason(row):
				print('\n\n\n\n\n\n', "FOUND THE PRESEASON",'\n\n\n\n\n\n')
				finalPage= 1
				break
		else:
			if regularSeason:
				gameObjects+= scrapeGame(row)
	#for game in gameObjects: print("GAME OBJECT: ", game, '\n')
	return (finalPage, gameObjects)


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

# Given a table row (which corresponds to an NBA game), 
# this function returns a list [homeGame,awayGame], where 
# 'homeGame' and 'awayGame' are Game objects corresponding to
# each game: one object from the perspective of the Home team,
# and one from the perspective of the Away team).
# !Currently doesn't record the date of the game yet!
def scrapeGame(row):

	#reference the global teamGames variable
	global teamGames

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

	#set the season start year 
	homeGame.seasonStartYear= currentSeasonStartYear
	awayGame.seasonStartYear= currentSeasonStartYear

	#set the game date (i.e. game number from 1 to [num games])
	teamGames[homeTeam]= teamGames.get(homeTeam, 0) + 1
	teamGames[awayTeam]= teamGames.get(awayTeam, 0) + 1
	homeGame.gameNumber= teamGames[homeTeam]
	awayGame.gameNumber= teamGames[awayTeam]
	
	print("Home game:")
	print(homeGame)
	print("\nAway game:")
	print(awayGame)
	print("\n\n\n\n")
	
	return [homeGame, awayGame]



if __name__ == '__main__':
	
	#url= "https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/2/"

	gameObjects= scrapeSeasons(2020,2022)
	#for game in gameObjects: print('\n',game,'\n\n')
	#getGameDataFromPage(soup)

	print('\n\n\n\n\n\n', "FINAL RESULTS: ", '\n\n\n\n')

	for i,game in enumerate(gameObjects): print(i, "  ", game, "\n\n")

	driver.quit()