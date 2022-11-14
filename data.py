#Game object must contain: 
#	"team": <team name (str)>
#   "date": <date of game (datetime)>
#   "outcome": <1 if team won, 0 if lost (int/bool)>
#   "odds": <moneyline (int)> 
class Game:

	def __init__(self, team=None, gameNumber=None, 
		outcome=None, winOdds=None, loseOdds=None):
		self.team = team
		self.gameNumber = gameNumber
		self.outcome = outcome
		self.winOdds = winOdds
		self.loseOdds = loseOdds

	def __str__(self):
		return f"Team: {self.team}, Outcome: {self.outcome}, WinOdds: {self.winOdds}, LoseOdds: {self.loseOdds}, GameNumber: {self.gameNumber}"