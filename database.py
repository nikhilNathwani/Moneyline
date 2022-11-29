import sqlite3

con = sqlite3.connect("moneyline.db")
cur = con.cursor()

def createGamesTable():
	#Specifying data types is optional. Can add later.
	cur.execute("CREATE TABLE games(team, seasonStartYear, gameNumber, outcome, winOdds, loseOdds)")

if __name__ == '__main__':
	#createGamesTable()
	con.close()
