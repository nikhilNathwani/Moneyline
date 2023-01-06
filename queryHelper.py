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
	#Unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= 1 if filters['outcome']=='win' else 0
	wager= filters['bet']

	#Create SQL query
	query = f"""SELECT COUNT(*)
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome <> {guessedOutcome}"""
	
	#Execute query and extract the COUNT value
	#Note that fetchall() returns list of tuples even if I'm just getting COUNT
	#E.g. [( <value of COUNT(*)> , <empty 2nd value> )]
	cursor.execute(query)
	count= cursor.fetchall()[0][0]

	#Calculate and return profit
	profit= count*wager
	print("LOSSES:", profit)
	return profit


def correctExpectedGuessProfit(cursor, filters):
	#Unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= 1 if filters['outcome']=='win' else 0
	wager= filters['bet']

	#Create SQL query
	query = f"""SELECT COUNT(*)
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome == {guessedOutcome};"""

	return 0

def correctUnexpectedGuessProfit(cursor, filters):
	#Unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= filters['outcome']=='win'
	wager= filters['bet']


	#Determine whether to looks at winOdds or loseOdds
	odds= "winOdds" if guessedOutcome=="win" else "loseOdds"

	#Create SQL query
	#Notes:
	# - Since I'm calculating "unexpected" guess profit, I need odds 
	#   to be positive. So I should add up instances where guessOutcome
	#   is correct, AND winOdds/loseOdds is positive (depending on whether
	#   I guessed a win or a loss, via the 'odds' variable above).
	query = f"""SELECT SUM({odds})
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome = {guessedOutcome}
			AND {odds}>0;"""
	
	#Execute query and extract the SUM value
	cursor.execute(query)
	oddsSum= cursor.fetchall()[0][0] #fetchall() returns [(<value of SUM>,)]

	#Calculate and return profit
	profit= oddsSum*wager/100
	print("EXPECTED EARNINGS:", profit)
	return profit

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