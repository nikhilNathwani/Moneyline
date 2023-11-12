from queryHelper import *
from flask import Flask, render_template, request, jsonify

#Columns: 
#team
#seasonStartYear
#gameNumber
#outcome
#winOdds
#loseOdds

moneyline_app = Flask(__name__, template_folder='templates')

@moneyline_app.route('/')
def index():
  return render_template('index.html')

#returns user-inputted values for betAmount, team, 
#gameOutcome, & seasonStartYear. "req" short for "request"
def getFilterValues():
    bet = request.args.get('bet',type=int)
    team = request.args.get('team')
    outcome = request.args.get('outcome')
    seasonStartYear= request.args.get('seasonStart',type=int)
    return {"bet":bet, "team":team, 
    "outcome":outcome, "seasonStartYear":seasonStartYear}    

@moneyline_app.route('/query')
def query_games():
    # Connect to the database
    conn = sqlite3.connect('data/moneyline.db')
    cursor = conn.cursor()

    # Get the filters from the query string
    filters= getFilterValues()

    # Execute the first query and fetch results
    allGames= getAllGames(cursor,filters)
    print("GAMES:\n",allGames, len(allGames))

    # Execute the second query and fetch results    
    profit= calculateProfit(cursor,filters)
    print("TOTAL PROFIT:",profit)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify({'games': allGames, 'profit': profit})


if __name__ == '__main__':
  moneyline_app.run(debug=True)
