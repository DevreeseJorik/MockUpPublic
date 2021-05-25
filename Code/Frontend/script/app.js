const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const listenToUIHome = function () {
  let cocktailButtons = document.querySelectorAll(".js-cocktail-button");
  console.log("Cocktailbuttons");
  console.log(cocktailButtons);
  for (let button of cocktailButtons) {
    // console.log(button);
    button.addEventListener("click",function () {
      let value = button.getAttribute("value");
      console.log(value);
      socket.emit('F2B_request_cocktail',{'cocktail_id':value});
  });
  }
};

const add_cocktails = function (jsonObject) {
  let htmlCocktail = document.querySelector(".cocktail_section");
  console.log(htmlCocktail);
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
  listenToUIHome();
}


const listenToSocketHome = function () {
  socket.on("connected", function () {
    console.log("Connection established.");
  });

  socket.on("B2F_cocktails", function (jsonObject) {
    console.log("Received cocktail list");
    console.log(jsonObject);
    add_cocktails(jsonObject);
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  let url = window.location.pathname.split('/');
  console.log(url);
  if ((url[1] == "Home.html") | (url[4] == "Home.html")) {
    listenToSocketHome();
  } else {
    console.log("Stat page is unfinished");
  }
});
