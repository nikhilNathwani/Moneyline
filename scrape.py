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
	time.sleep(5)
	html= driver.page_source
	return BeautifulSoup(html,'lxml')


#Leaving date aside for now
def getGameDataFromPage(soup):
	table= soup.find("table", "table-main")
	rows= table.find_all_next("tr", {"class":["deactivate", 'nob-border']})
	date= None
	for row in rows: 
		if(isDateRow(row)):
			date= parseDate(row)
		else: 
			scrapeGame(row, date)
	return rows

def isDateRow(row):
	return 'nob-border' in row.get("class")

def parseDate(row):
	dateObject= row.find("span", class_="datet")
	day,month,year= dateObject.text.split(" ")
	#convert month abbreviation to number using 'calendar' library
	year= int(year)
	month= int(list(calendar.month_abbr).index(month))
	day= int(day)
	return date(year,month,day) 

# Given a table row (which corresponds to an NBA game), 
# this function returns a list [homeGame,awayGame], where 
# 'homeGame' and 'awayGame' are Game objects corresponding to
# each game: one object from the perspective of the Home team,
# and one from the perspective of the Away team).
# !Currently doesn't record the date of the game yet!
def scrapeGame(row, date):
	#initialize the 2 Game objectes
	homeGame= Game()
	awayGame= Game()

	#set the game date
	homeGame.date= date
	awayGame.date= date

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
	
	url= "https://www.oddsportal.com/basketball/usa/nba-2021-2022/results/#/page/2/"

	print("Making soup...")
	soup= makeSoup(url)
	print("Made soup")

	print("Getting table data...")
	#getGameDataFromPage(soup)
	dates= soup.find_all("tr",class_="nob-border")
	print("Dates: ", dates)
	for date in dates:
		print('\n',date,'\n',date.find('span').text,'\n\n')

	driver.quit()