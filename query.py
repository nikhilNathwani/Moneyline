#Quick queries to validate the data 

from database import *

#Columns: 
#team
#seasonStartYear
#gameNumber
#game.outcome
#game.winOdds
#game.loseOdds


#Calculate # games played per team per season
def verifyGameCounts():
	#First just calculating # of wins
	res= cur.execute("""
		SELECT team, seasonStartYear, MAX(gameNumber) AS gamesPlayed
		FROM games
		GROUP BY seasonStartYear, team 
		ORDER BY seasonStartYear DESC, team ASC;
		""")
	return res.fetchall()


#Calculate # games won per team per season
def verifyWinCounts():
	#First just calculating # of wins
	res= cur.execute("""
		SELECT team, seasonStartYear, SUM(outcome) AS wins
		FROM games
		GROUP BY seasonStartYear, team 
		ORDER BY team ASC, seasonStartYear DESC;
		""")
	return res.fetchall()


if __name__ == '__main__':
	for r in verifyGameCounts():
		print(r)
	con.close()