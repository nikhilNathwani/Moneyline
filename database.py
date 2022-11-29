import sqlite3
from Game import game

con = sqlite3.connect("moneyline.db")
cur = con.cursor()

def createGamesTable():
	#Specifying data types is optional. Can add later.
	cur.execute("CREATE TABLE games(team, seasonStartYear, gameNumber, outcome, winOdds, loseOdds)")

#Converts Game object into a list of its attributes, in the appopriate
#order for getting inserted into the 'games' table of moneyline.db
def listifyGame(game):
	return [game.team, game.seasonStartYear, game.gameNumber, game.outcome, game.winOdds, game.loseOdds]

#Same as listifyGame() but for a list of multiple Game objects
def listifyGames(gameList):
	result=[]
	for game in gameList:
		result += listifyGame(game)
	return result

if __name__ == '__main__':
	#createGamesTable()
	con.close()
