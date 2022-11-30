#Quick queries to validate the data 

from database import *

#Columns: 
#team
#seasonStartYear
#gameNumber
#game.outcome
#game.winOdds
#game.loseOdds


#Calculate # games played and won per team per season
def verifyGameCounts():
	#First just calculating # of wins
	res= cur.execute("""
		
		SELECT team, seasonStartYear, SUM(outcome) 
		FROM games
		WHERE seasonStartYear != 2019
		GROUP BY seasonStartYear, team 
		ORDER BY team ASC, seasonStartYear DESC

		""")
	return res.fetchall()



if __name__ == '__main__':
	for r in verifyGameCounts():
		print(r)
	con.close()