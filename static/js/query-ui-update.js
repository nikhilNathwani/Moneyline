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
      makeTotalProfitUI(response.profit);
      makeRawDataUI(response.games);  
    });
}

function makeTotalProfitUI(profit) {
  // Set up the results container
  const totalProfitUI = document.getElementById('total-profit-UI');
  totalProfitUI.innerHTML = '';

  //Create the 'then you would have won' text
  const caption= document.createElement('span');
  caption.id = "caption-text";
  caption.innerText = "Then you would have...";
  totalProfitUI.appendChild(caption);

  return;
}

function makeRawDataUI(games) {
  console.log(games);

  // Set up the results container
  const rawDataUI = document.getElementById('raw-data-UI');
  rawDataUI.innerHTML = '';

  // Loop through the games and create a new element for each one
  games.forEach(game => {
    const gameElement = document.createElement('div');
    gameElement.innerHTML = `${game[0]} - ${game[1]} - ${game[2]} - ${game[3]} - ${game[4]} - ${game[5]}`;
    rawDataUI.appendChild(gameElement);
  });

  rawDataUI.appendChild(document.createElement('br'))
  rawDataUI.appendChild(document.createElement('br'))
}
