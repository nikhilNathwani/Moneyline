from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data import Game

#Scrape results from 2021-2022 regular season


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
		print("\n\n")
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
	print(teamString)
	print(homeTeam)
	print(awayTeam)
	print("\n\n")

	#set the winner/loser
	winner= teams.find("span","bold").text
	homeGame.outcome= int(winner==homeTeam)
	awayGame.outcome= int(winner==awayTeam)
	'''	print("Winner: " + winner)
	print("Home won?")
	print(winner == homeTeam)
	print(homeGame.outcome)
	print("Away won?")
	print(winner == awayTeam)
	print(awayGame.outcome)
	print("\n\n")'''

	#set the odds
	odds= row.find_all("td","odds-nowrp")
	homeOdds,awayOdds= [odd.text for odd in odds]
	homeGame.odds= homeOdds
	awayGame.odds= awayOdds
	print(odds)
	print(homeGame.odds)
	print(awayGame.odds)
	print("\n\n\n\n\n\n")







if __name__ == '__main__':
	print("Making soup...")
	soup= makeSoup("https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/3/")
	print("Made soup")

	print("Getting table data...")
	games= getAllGameData(soup)
	#print(games)

	driver.quit()