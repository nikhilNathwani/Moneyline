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
	query = 'SELECT * FROM games'
	where_clauses = []
	if team != None:
		where_clauses.append(f'team = "{team}"')
	if seasonStartYear != None:
		where_clauses.append(f'seasonStartYear = {seasonStartYear}')
	if where_clauses != []:
		query += ' WHERE ' + ' AND '.join(where_clauses)
	cursor.execute(query)
	return cursor.fetchall()	

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