// Set up the submit button, and ensure it is
// loaded before adding its event listener
document.addEventListener('DOMContentLoaded', () => {
  const submitButton = document.getElementById('submit-button');
  submitButton.addEventListener('click', queryGames);
});

function queryGames() {

  // Get the values of the UI filters
  const bet = document.getElementById('bet-input').value; 
  const team = document.getElementById('team-input').value;
  const outcome = document.getElementById('outcome-input').value; 
  const seasonStartYear = document.getElementById('season-input').value;

  // Make a request to the /query route, passing the filters as parameters
  fetch(`/query?bet=${bet}&team=${team}&outcome=${outcome}&seasonStart=${seasonStartYear}`)
    .then(response => response.json())  
    .then(response => {
      makeTotalProfitBox(response.profit);
      makeRawDataBox(response.games);  
    });
}

function makeTotalProfitBox(profit) {
  // Set up the results container
  const totalProfitBox = document.getElementById('total-profit-box');
  totalProfitBox.innerHTML = '';

  //Create the 'then you would have won' text, i.e. the "pre-text"
  const preText= document.createElement('span');
  preText.id = "pre-text";
  preText.innerText = "Then you would have...";
  totalProfitBox.appendChild(preText);

  //Create the '[won/lost] [profit $ amount]' text, i.e. the "result-text"
  const resultText= document.createElement('span');
  resultText.id = "result-text";
  resultText.innerText = "Won " + profit;
  totalProfitBox.appendChild(resultText);

  return;
}


function makeRawDataBox(games) {
  console.log(games);

  // Set up the results container
  const rawDataBox = document.getElementById('raw-data-box');
  rawDataBox.innerHTML = '';

  // Loop through the games and create a new element for each one
  games.forEach(game => {
    const gameElement = document.createElement('div');
    gameElement.innerHTML = `${game[0]} - ${game[1]} - ${game[2]} - ${game[3]} - ${game[4]} - ${game[5]}`;
    rawDataBox.appendChild(gameElement);
  });

  rawDataBox.appendChild(document.createElement('br'))
  rawDataBox.appendChild(document.createElement('br'))
}
