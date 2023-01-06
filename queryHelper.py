#SQL queries to help app.py return pre-calculated values
import sqlite3

#Columns: 
#team
#seasonStartYear
#gameNumber
#outcome
#winOdds
#loseOdds

def getAllGames(cursor, filters):
	# Build the SELECT query using the filters
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	
	query = f"""SELECT *
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}"""

	cursor.execute(query)
	return cursor.fetchall()	

def calculateEarnings(cursor, filters):
	losses= incorrectGuessProfit(cursor,filters) 
	earningsExpected= correctExpectedGuessProfit(cursor,filters)
	earningsUnexpected= correctUnexpectedGuessProfit(cursor,filters)
	return earningsExpected + earningsUnexpected - losses

def incorrectGuessProfit(cursor, filters):
	#unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= 1 if filters['outcome']=='win' else 0
	wager= filters['bet']

	#Create SQL query
	query = f"""SELECT COUNT(*)
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome = {guessedOutcome}"""
	
	#Execute query and extract the 
	#Note that fetchall() returns list of tuples even if I'm just getting COUNT
	#E.g. [( <value of COUNT(*)> , <empty 2nd value> )]
	cursor.execute(query)
	count= cursor.fetchall()[0][0]

	#Calculate profit
	profit= count*wager
	print("LOSSES:", profit)
	return profit


def correctExpectedGuessProfit(cursor, filters):
	return 0

def correctUnexpectedGuessProfit(cursor, filters):
	return 0

#only works for a "win" prediction
def getEarningsQueryString(filters):
	betTableQuery= f"""WITH betTable
		AS
		(SELECT outcome, winOdds, gameNumber,
			{filters['bet']} AS wager,
			(SIGN(winOdds)+1)/2 AS isUnderdog,
			1-((SIGN(winOdds)+1)/2) AS isFavorite
		FROM games
		WHERE team='{filters['team']}' AND seasonStartYear='{filters['seasonStartYear']}'
		), """

	payoutPerGameQuery= f"""payouts
		AS
		(SELECT outcome, winOdds, wager, gameNumber,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) AS payout,
			(outcome)*(isUnderdog*(wager/100)*(winOdds+100) + isFavorite*(wager/ABS(winOdds))*(100+ABS(winOdds))) - wager AS profit
		FROM betTable
		) 
		"""

	payoutPerSeasonQuery= f"""
		SELECT MAX(gameNumber) AS totalGames,
			SUM(wager) AS totalWager,
			ROUND(SUM(payout),2) AS totalPayout, 
			ROUND(SUM(profit),2) AS totalProfit
		FROM payouts
	;"""
	print("Query:\n",betTableQuery + payoutPerGameQuery + payoutPerSeasonQuery)
	return betTableQuery + payoutPerGameQuery + payoutPerSeasonQuery