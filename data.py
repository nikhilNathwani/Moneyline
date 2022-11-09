#Game object must contain: 
#	"team": <team name (str)>
#   "date": <date of game (datetime)>
#   "outcome": <1 if team won, 0 if lost (int/bool)>
#   "odds": <moneyline (int)> 
class Game:
	
	def __init__(self):
		self.team = None
		self.date = None
		self.outcome = None 
		self.odds = None


	def __init__(self, team, date, outcome, odds):
		self.team = team
		self.date = date
		self.outcome = outcome
		self.odds = odds


	'''def __str__(self):
		return f"{self.name}({self.age})"'''