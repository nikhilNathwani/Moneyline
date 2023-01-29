// Set up the submit button, and ensure it is
// loaded before adding its event listener
const submitButton = document.getElementById('submit-button');
submitButton.addEventListener('click', function() {
  window.scrollTo({
    top: document.getElementById("summary-page").offsetTop,
    behavior: "smooth"
  });
  queryGames();
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
      makeRawDataBox(response.games);  
    });
}

function makeTotalProfitUI(profit) {
  // Set up the results container
  const totalProfitDiv = document.getElementById('total-profit-div');
  totalProfitDiv.innerHTML = '';

  //Create the 'then you would have won' text, i.e. the "pre-text"
  const preText= document.createElement('span');
  preText.id = "pre-text";
  preText.innerText = "...then your total profit would be";
  totalProfitDiv.appendChild(preText);

  //Create the '[+/-] [profit $ amount]' text, i.e. the "result-text"
  const resultText= document.createElement('span');
  resultText.id = "result-text";
  profitTextAnimation(resultText, profit);
  resultText.style.color= profit<0 ? "red" : "green";
  totalProfitDiv.appendChild(resultText);

  //Create the 'by the end of the season' text, i.e. the "post-text"
  const postText= document.createElement('span');
  postText.id = "post-text";
  postText.innerText = "at the end of the season!";
  totalProfitDiv.appendChild(postText);
}

function profitTextHelper(profit) {
  if (profit < 0) {
    return {"text":"-$" + (-1*profit).toFixed(2), "color":"red"};
  } 
  else {
    return {"text":"+$" + profit.toFixed(2), "color":"green"};
  }
}

function profitTextAnimation(profitSpan,profitAmount) {
  //Animation variables
  var current = 0; // the current dollar amount
  var increment = 1; // the amount to increment by
  var speed = 1; // the animation speed in milliseconds

  //Positive/negative profit variables
  var profitAbsVal= profitAmount < 0 ? -profitAmount : profitAmount;
  var sign= profitAmount < 0 ? "-" : "+";
  
  profitSpan.innerHTML = "$" + current;
  console.log(current, profitAmount);

  var animate = setInterval(function(){
      current += increment;
      profitSpan.innerHTML = sign + "$" + current.toFixed(2);
      if(current >= profitAbsVal){
          profitSpan.innerHTML = sign + "$" + profitAbsVal.toFixed(2);
          clearInterval(animate);
      }
  }, speed);  
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
