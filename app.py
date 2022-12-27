import sqlite3
from flask import Flask, render_template, request, jsonify

#Columns: 
#team
#seasonStartYear
#gameNumber
#outcome
#winOdds
#loseOdds

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/query')
def query_games():
    # Connect to the database
    conn = sqlite3.connect('data/moneyline.db')
    cursor = conn.cursor()

    # Get the filters from the query string
    betAmount_filter = request.args.get('bet',type=int)
    team_filter = request.args.get('team')
    gameOutcome_filter = request.args.get('outcome',type=int)
    seasonStartYear_filter= request.args.get('seasonStart',type=int)
    print("Bet:", betAmount_filter)
    print("Team:", team_filter)
    print("Outcome:", gameOutcome_filter)
    print("Season Start:", seasonStartYear_filter)

    # Build the SELECT query using the filters
    query = 'SELECT * FROM games'
    where_clauses = []
    if team_filter:
        where_clauses.append(f'team = "{team_filter}"')
    if gameOutcome_filter:
        where_clauses.append(f'outcome = {gameOutcome_filter}')
    if seasonStartYear_filter:
        where_clauses.append(f'seasonStartYear = {seasonStartYear_filter}')
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)

    print("Query:", query)

    # Execute the SELECT query
    cursor.execute(query)

    # Fetch the results of the query
    games = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(games)


if __name__ == '__main__':
  app.run(debug=True)
