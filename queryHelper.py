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
	earningsUnexpected= correctUnexpectedGuessProfit(cursor,filters)
	earningsExpected= correctExpectedGuessProfit(cursor,filters)
	profit= earningsUnexpected + earningsExpected - losses
	profit= profit - profit%0.01 #round down to nearest cent
	return profit

def incorrectGuessProfit(cursor, filters):
	#Unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= filters['outcome']=='win' #1 if "win", else 0
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
	guessedOutcome= filters['outcome']
	wager= filters['bet']

	#Determine whether to look at winOdds or loseOdds
	odds= "winOdds" if guessedOutcome=="win" else "loseOdds"

	#Now set guessedOutcome to 0/1 for my SQL query
	guessedOutcome= int(filters['outcome']=="win")

	#Create SQL query
	#Notes:
	# - Since I'm calculating "expected" guess profit, I need odds 
	#   to be negative. So I should add up instances where guessOutcome
	#   is correct, AND winOdds/loseOdds is negative (depending on whether
	#   I guessed a win or a loss, via the 'odds' variable above).
	# - I'm adding together the winOdds/loseOdds, but they are stored as 
	#   strings e.g. "+120" and "-150", so before taking the SUM I need to
	#   get the proper substring and cast to an integer
	query = f"""SELECT SUM(1.0/CAST(SUBSTR({odds}, 2) AS INTEGER))
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome = {guessedOutcome}
			AND SUBSTR({odds},1,1) = '-';"""
		
	#Execute query and extract the SUM value
	cursor.execute(query)
	oddsReciprocalSum= cursor.fetchall()[0][0] #fetchall() returns [(<value of SUM>,)]

	#Calculate and return profit
	profit= oddsReciprocalSum*wager*100.0
	print("EXPECTED EARNINGS:", profit)
	return profit

def correctUnexpectedGuessProfit(cursor, filters):
	#Unpack 'filters' object
	team= filters['team']
	seasonStartYear= filters['seasonStartYear']
	guessedOutcome= filters['outcome']
	wager= filters['bet']

	#Determine whether to look at winOdds or loseOdds
	odds= "winOdds" if guessedOutcome=="win" else "loseOdds"

	#Now set guessedOutcome to 0/1 for my SQL query
	guessedOutcome= int(filters['outcome']=="win")

	#Create SQL query
	#Notes:
	# - Since I'm calculating "unexpected" guess profit, I need odds 
	#   to be positive. So I should add up instances where guessOutcome
	#   is correct, AND winOdds/loseOdds is positive (depending on whether
	#   I guessed a win or a loss, via the 'odds' variable above).
	# - I'm adding together the winOdds/loseOdds, but they are stored as 
	#   strings e.g. "+120" and "-150", so before taking the SUM I need to
	#   get the proper substring and cast to an integer
	query = f"""SELECT SUM(CAST(SUBSTR({odds}, 2) AS INTEGER))
			FROM games
			WHERE team = "{team}"
			AND seasonStartYear = {seasonStartYear}
			AND outcome = {guessedOutcome}
			AND SUBSTR({odds},1,1) = '+';"""

	#Execute query and extract the SUM value
	cursor.execute(query)
	oddsSum= cursor.fetchall()[0][0] #fetchall() returns [(<value of SUM>,)]

	#Calculate and return profit
	profit= oddsSum*wager/100.0
	print("UNEXPECTED EARNINGS:", profit)
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