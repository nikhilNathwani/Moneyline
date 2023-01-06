#Quick queries to validate the data 

from database import *

#Columns: 
#team
#seasonStartYear
#gameNumber
#outcome
#winOdds
#loseOdds


#Calculate # games played per team per season
def verifyGameCounts():
	res= cur.execute("""
		SELECT team, seasonStartYear, MAX(gameNumber) AS gamesPlayed
		FROM games
		GROUP BY seasonStartYear, team 
		ORDER BY seasonStartYear DESC, team ASC;
		""")
	return res.fetchall()


#Calculate # games won per team per season
def verifyWinCounts():
	res= cur.execute("""
		SELECT team, seasonStartYear, SUM(outcome) AS wins
		FROM games
		GROUP BY seasonStartYear, team 
		ORDER BY team ASC, seasonStartYear DESC;
		""")
	return res.fetchall()


#Calculate earnings if I bet $X on team T to Z[win/lose] each game of year Y
#Starting with static T,X,Y,Z: 2021, $100, Celtics, Win
def calculatePayoutPerGame():
	res= cur.execute("""
		WITH betResults
		AS
		(SELECT seasonStartYear, gameNumber, team, outcome, winOdds,
			100 AS wager,
			(SIGN(winOdds)+1)/2 AS isUnderdog,
			1-((SIGN(winOdds)+1)/2) AS isFavorite
		FROM games
		)
		SELECT seasonStartYear, gameNumber, team, outcome, winOdds, wager,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) AS payout,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) - wager AS profit
		FROM betResults
		WHERE team='Boston Celtics' AND seasonStartYear=2021
		ORDER BY team ASC, gameNumber ASC;
		""")
	return res.fetchall()


def calculatePayoutPerSeason():
	res= cur.execute("""
		WITH betResults
		AS
		(SELECT seasonStartYear, gameNumber, team, outcome, winOdds,
			100 AS wager,
			(SIGN(winOdds)+1)/2 AS isUnderdog,
			1-((SIGN(winOdds)+1)/2) AS isFavorite
		FROM games
		),
		payouts
		AS 
		(SELECT seasonStartYear, gameNumber, team, outcome, winOdds, wager,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) AS payout,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) - wager AS profit
		FROM betResults
		)
		SELECT seasonStartYear, team, 
			MAX(gameNumber) AS totalGames,
			SUM(wager) AS totalWager,
			ROUND(SUM(payout),2) AS totalPayout, 
			ROUND(SUM(profit),2) AS totalProfit
		FROM payouts
		GROUP BY seasonStartYear, team
		ORDER BY team ASC, seasonStartYear DESC;
		""")
	return res.fetchall()


if __name__ == '__main__':
	for r in calculatePayoutPerSeason():
		print(r)
	con.close()