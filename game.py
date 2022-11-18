#Game object must contain: 
#	"team": <team name (str)>
#	"seasonStartYear": <calendar year in which the season started (int)>
#	"gameNumber": <num of game within the season i.e. 1st game is 1, 2nd is 2, etc. (int)>
#   "date": <date of game (datetime)>
#   "outcome": <1 if team won, 0 if lost (int/bool)>
#   "odds": <moneyline (int)> 
class Game:
	def __init__(self, team=None, seasonStartYear= None, gameNumber=None, 
		outcome=None, winOdds=None, loseOdds=None):
		self.team = team
		self.seasonStartYear= seasonStartYear
		self.gameNumber = gameNumber
		self.outcome = outcome
		self.winOdds = winOdds
		self.loseOdds = loseOdds

	def __str__(self):
		return f"Season: '{self.seasonStartYear%100}-'{(self.seasonStartYear+1)%100}, Team: {self.team}, Outcome: {self.outcome}, WinOdds: {self.winOdds}, LoseOdds: {self.loseOdds}, GameNumber: {self.gameNumber}"