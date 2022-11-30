import sqlite3
from game import Game

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
		result.append(listifyGame(game))
	return result

def addGamesToGamesDB(gameObjectList):
	print("\n\n\nADDING games to database")
	gamesList= listifyGames(gameObjectList)
	cur.executemany("INSERT INTO games VALUES(?,?,?,?,?,?)", gamesList)
	con.commit()
	print("DONE ADDING games to database")


if __name__ == '__main__':
	createGamesTable()
	con.close()
