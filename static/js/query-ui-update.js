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
  preText.innerText = "Then your total profit would be";
  totalProfitBox.appendChild(preText);

  //Create the '[won/lost] [profit $ amount]' text, i.e. the "result-text"
  const resultText= document.createElement('span');
  resultText.id = "result-text";
  profitResult= profitTextHelper(profit);
  resultText.innerText = profitResult.text;
  resultText.style.color= profitResult.color;
  totalProfitBox.appendChild(resultText);

  //Create the 'by the end of the season' text, i.e. the "post-text"
  const postText= document.createElement('span');
  postText.id = "post-text";
  postText.innerText = "at the end of the season!";
  totalProfitBox.appendChild(postText);
}

function profitTextHelper(profit) {
  if (profit < 0) {
    return {"text":"-$" + -1*profit, "color":"red"};
  } 
  else {
    return {"text":"+$" + profit, "color":"green"};
  }
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
