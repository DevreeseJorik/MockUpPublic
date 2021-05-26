const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const listenToUIMenu = function () {
  let cocktailButtons = document.querySelectorAll(".js-cocktail-button");
  // console.log("Cocktailbuttons");
  // console.log(cocktailButtons);
  for (let button of cocktailButtons) {
    // console.log(button);
    button.addEventListener("click",function () {
      let value = button.getAttribute("value");
      console.log(value);
      socket.emit('F2B_request_cocktail',{'cocktail_id':value});
  });
  }
};

const addCocktails = function (jsonObject) {
  let htmlCocktail = document.querySelector(".cocktail_section");
  // console.log(htmlCocktail);
  let dataCocktails = "";
  for (let cocktail of jsonObject.cocktails) {

    let rowOrder = "";

    if (cocktail.cocktailId %2 == 0) {
      rowOrder = "-reverse";
    };

    dataCocktails += `<article class="o-row o-row--lg">
                    <div class="o-container">
                        <div class="o-layout o-layout--gutter-lg o-layout--align-center o-layout--row${rowOrder}">
                            <div class="o-layout__item u-1-of-2-bp3 u-2-of-5-bp4">
                                <figure class="c-figure">
                                    <img src="img/cocktail_${cocktail.cocktailId}.png" alt="visual of cocktail">
                                </figure>
                            </div>
                            <div class="o-layout__item u-1-of-2-bp3 u-2-of-5-bp4">
                                <div class="u-max-width-sm">
                                    <h2 class="c-lead c-lead--lg">
                                        ${cocktail.name} - ${Math.round(cocktail.alcoholPercentage*10**4)/10**2}% vol
                                    </h2>
                                    <p class="u-mb-lg u-typography-secondary-base">
                                        ${cocktail.description}      
                                    <p>
                                        <a class="c-link-lm js-cocktail-button" href="#!" value="${cocktail.cocktailId}">
                                            Try it out
                                        </a>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>`
  };
  htmlCocktail.innerHTML = dataCocktails;
  listenToUIMenu();
}

const addAnalytics = function() {
  let htmlAnalytics = document.querySelector(".analytics_section");
  console.log(htmlAnalytics);
  console.log("What")

  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
          datasets: [{
              label: '# of Votes',
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
}

const addDeviceData = function(jsonObject) {
  let htmlDevice = document.querySelector(".analytics_section")
  htmlDevice.innerHTML = ""
  for (let device of jsonObject.history) {
    htmlDevice.innerHTML += `Name: ${device.name}\nValue: ${device.value}\nDescription: ${device.description}`
  }
  socket.emit('F2B_history_device',{'limit':1});

}


const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("Connection established.");
  });

  let url = window.location.pathname.split('/');
  // console.log(url);  
  if ((url[1] == "Menu.html") | (url[4] == "Menu.html")) {
    console.log("Welcome to the Menu Page.");
    socket.emit('F2B_request_data',{'url':"Menu.html"});
    listenToSocketMenu();
    
  } 
  
  if ((url[1] == "Stats.html") | (url[4] == "Stats.html")) {
    console.log("Welcome to the Analytics Page");
    socket.emit('F2B_request_data',{'url':"Stats.html","limit":1});
    listenToSocketStat();
  }


};

const listenToSocketMenu = function() {
  socket.on("B2F_cocktails", function (jsonObject) {
    console.log("Received cocktail list");
    console.log(jsonObject);
    addCocktails(jsonObject);
  });
};

const listenToSocketStat = function() {
  socket.on("B2F_analytics", function (jsonObject) {
    console.log("Received Analytics list");
    // console.log(jsonObject);
    addAnalytics();
    addDeviceData(jsonObject);
  });

  socket.on("B2F_history_device", function (jsonObject) {
    // console.log("Received latest history");
    // console.log(jsonObject);
    addDeviceData(jsonObject);
  });
};



document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToSocket();
});
