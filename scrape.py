from scrapeUtil import *
from game import Game
from database import *

#Scrape game results and odds from NBA regular seasons

#Notes:
#1) oddsportal.com takes an average moneyline across many bookers
#2) oddsportal.com seems to have the dates of games all wrong. But
#   this isn't necessarily a deal-breaker. I don't care about the 
#   exact date, I just care about the order of the games. So I'll
#   try to number the game dates from 0 to [num games] for each team. 

#Global variables
currentSeasonStartYear= 0
teamGames= {}


#Scrapes NBA seasons from [startYear]-[startYear+1] to [endYear-1]-[endYear]
#(one season at a time, since they're at different URLs)
#Then adds the resulting Game objects to the 'games' table in moneyline.db
def scrapeSeasons(startYear,endYear):
	global currentSeasonStartYear
	global teamGames
	allGameObjects= []
	y= startYear
	while y < endYear:
		currentSeasonStartYear= y
		gameObjectsFromSeason= scrapeSeason(y)
		fixGameNumbers(gameObjectsFromSeason) #comment in scrapeGame() explains why
		allGameObjects+= gameObjectsFromSeason
		teamGames= {} #so that gameNum counts reset before scraping the next season
		y+= 1
	#Add all Game objects to 'games' table of moneyline.db
	addGamesToGamesDB(allGameObjects)
	return allGameObjects


#Scrapes the [startYear]-[startYear+1] NBA season
#(traverses through multiple pages of data within that season)
def scrapeSeason(startYear):
	print("STARTING season",currentSeasonStartYear,"-",(currentSeasonStartYear+1))
	urlBase= "https://www.oddsportal.com/basketball/usa/nba-"
	urlBase+= str(startYear)+"-"+str(startYear+1)+"/results/#/page/"
	pageNum= 1
	doneTraversing= 0
	allGameObjects= []
	while not doneTraversing:
		url= urlBase+str(pageNum)+"/"
		print("SCRAPING PAGE", pageNum)
		isFinalPage,gameObjectsFromPage= scrapePage(url)
		allGameObjects+= gameObjectsFromPage
		pageNum+= 1
		doneTraversing= isFinalPage
	return allGameObjects


#Returns tuple (finalPage <bool>, gameObjects <list>), where:
# - 'finalPage' is 1 if this was the last page to scrape for the given season
# - 'gameObjects' is the list of all Game objects scraped from the given page
def scrapePage(url):
	soup= makeSoup(url)
	table= soup.find("table", "table-main")
	#Game rows have class "deactivate". Header rows have class "nob-border".
	#Header rows indicate whether the next games are playoffs/preseason/etc.
	rows= table.find_all_next("tr", {"class":["deactivate", 'nob-border']})
	gameObjects= []
	regularSeason= 0
	finalPage=0 
	for row in rows:
		#If looking at a header row, assess whether it's regular season or not.
		#And if it's preseason, that means we're done scraping reg season games.
		if isHeaderRow(row):
			regularSeason= isRegularSeason(row)
			if isPreSeason(row):
				if not is2020(row) and currentSeasonStartYear!=2019:
					print("FINISHED season",currentSeasonStartYear,"-",(currentSeasonStartYear+1),'\n\n\n\n\n\n')
					finalPage= 1
					break
		#If looking at a game row, scrape the game and add to gameObjects list
		else:
			if regularSeason:
				gameObjects+= scrapeGame(row)
	return (finalPage, gameObjects)


# Given a table row (which corresponds to an NBA game), this function 
# returns a list [homeGame,awayGame], where 'homeGame' and 'awayGame' 
# are Game objects corresponding to each game: one object from the perspective 
# of the Home team, and one from the perspective of the Away team).
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
	try:
		winner= teams.find("span","bold").text
	except (AttributeError):
		return []
	else:
		homeGame.outcome= int(winner==homeTeam)
		awayGame.outcome= int(winner==awayTeam)
	#^the 'try' catches an isolated issue in 2020 where some games got 
	#cancelled at the start of covid, and there was no winner or loser. 
	#In this case, return [] so that nothing gets added to gameObjects

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
	#Note: games are scraped in reverse chronological order, e.g. game 
	#82 actually gets a gameNumber of 1, and vice versa. Call function
	#fixGameNumbers() to fix this, after scraping the full season.
	
	return [homeGame, awayGame]


#Reverse gameNumbers so that they're written in ascending chronological order.
def fixGameNumbers(gameObjects):
	for game in gameObjects:
		game.gameNumber= teamGames[game.team] - game.gameNumber + 1


if __name__ == '__main__':
	gameObjects= scrapeSeasons(2016,2022)
	endScrape()
	con.close()