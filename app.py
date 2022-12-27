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
def query_users():
    # Connect to the database
    conn = sqlite3.connect('moneyline.db')
    cursor = conn.cursor()

    # Get the filters from the query string
    betAmount_filter = request.args.get('betAmount')
    team_filter = request.args.get('team')
    gameOutcome_filter = request.args.get('gameOutcome')
    seasonStartYear_filter= request.args.get('seasonStartYear')

    # Build the SELECT query using the filters
    query = 'SELECT * FROM users'
    where_clauses = []
    if name_filter:
        where_clauses.append(f'name = "{name_filter}"')
    if email_filter:
        where_clauses.append(f'email = "{email_filter}"')
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)

    # Execute the SELECT query
    cursor.execute(query)

    # Fetch the results of the query
    users = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(users)


if __name__ == '__main__':
  app.run(debug=True)
