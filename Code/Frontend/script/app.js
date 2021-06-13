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
  console.log(screen.width)

  if (screen.width > 997) {
    for (let cocktail of jsonObject.cocktails) {
      if (cocktail.cocktailId != 0) {

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
                                    <p class="u-mb-lg u-typography-secondary-base wide-screen-only">
                                      ${cocktail.description}      
                                    <p>
                                    <a class="c-link-lm js-cocktail-button" href="#!" value="${cocktail.cocktailId}">
                                      Make Cocktail
                                    </a>
                                    </p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </article>`;
      };
    };

  } else {
    for (let cocktail of jsonObject.cocktails) {
      let alcoholPercentage = Math.round(cocktail.alcoholPercentage*10**4)/10**2;
      let alcoholPercentageString = `${alcoholPercentage} % vol.`
      if (alcoholPercentage == 0) {
        alcoholPercentageString = `?`
      }

      if (cocktail.cocktailId %2 == 0) {
        dataCocktails += `<article class="o-row">
                            <div class="o-container">
                              <div class="o-layout o-layout--align-center o-layout--row">`;
      }; 

      dataCocktails += `<div class="o-layout__item u-1-of-2-bp3 u-2-of-5-bp4">
                          <div class="u-max-width-xl c-cocktail js-cocktail-button" value="${cocktail.cocktailId}">
                            <img class="c-cocktail-img" src="img/cocktail${cocktail.cocktailId}.png">
                            <div class="c-cocktail-txt c-cocktail-name">
                              <span>${cocktail.name}</span>
                            </div>
                            <p class="c-cocktail-txt c-cocktail-alc">${alcoholPercentageString}</p>
                            <div class="c-cocktail-txt c-cocktail-make">
                              <span>Make cocktail</span>
                            </div>
                          </div>
                        </div>`;

      if (cocktail.cocktailId %2 == 1) {
      dataCocktails +=  `</div>
                        </div>
                        </div>
                        </div>
                        </article>`;
      };
    };
  };
  htmlCocktail.innerHTML = dataCocktails;
  listenToUIMenu();
}

const showCurrentTemperature = function(temperature) {
  let htmlDevice = document.querySelector(".js-temperature")
  console.log(temperature)
  htmlDevice.innerHTML = `Temperature: ${temperature}°C`
  socket.emit('F2B_current_temperature',{'limit':1});
}


const showCocktailPopularity = function(jsonObject) {
  // console.log(jsonObject);
  let convertedCategories= [];
  let convertedData = [];
  for (const element of jsonObject) {
    // console.log(element);
    convertedCategories.push(element.name);
    convertedData.push(element.count);
  };

  drawBarChart(convertedCategories,convertedData,'.js-chart-cocktail-popularity',"Cocktail Popularity","");
}

const showHistorySensors = function(jsonObject) {
  console.log(jsonObject)
  let convertedCategoriesTemp= [];
  let convertedDataTemp  = [];

  let convertedCategoriesVolume= [];
  let convertedDataVolume  = [];

  if (jsonObject.length != 0) {
    for (const element of jsonObject.temperature) {
      convertedCategoriesTemp.push(element.time);
      convertedDataTemp.push(element.value);
    };
    drawLineChart(convertedCategoriesTemp,convertedDataTemp,'.js-chart-temperature','Time','Temperature','Temperature measurements',10,36);
    for (const element of jsonObject.volume) {
      convertedCategoriesVolume.push(`Drink ${element.deviceId}`);
      convertedDataVolume.push(element.value);
    };
    drawBarChart(convertedCategoriesVolume,convertedDataVolume,'.js-chart-volumes','Volume measurements');
  };
}

const showHistoryCocktail = function(jsonObject) {
  console.log(jsonObject)
  let convertedCategories= [];
  let convertedData  = [];

  if (jsonObject.length != 0) {
    for (const element of jsonObject) {
      convertedCategories.push(element.date);
      convertedData.push(element.historyId);
    };

    drawLineChart(convertedCategories,convertedData,'.js-chart-cocktail-history','Time','Cocktails','Cocktails History');

  };
};

const showHistoryActuator = function(jsonObject) {
  // console.log(jsonObject)

  let convertedCategories= [];
  let convertedData  = {0:[],1:[],2:[],3:[],4:[],5:[]};

  if (jsonObject.length != 0) {
    for (const element of jsonObject) {
      // console.log(element);
      // console.log(element.date);
      // console.log(element.value);
      id = element.deviceId-2;
      convertedCategories.push(element.time);
      convertedData[id].push(element.value);
      for (let i = 0; i < 6; i++) {
        if (i != id) {
          convertedData[i].push(0);
        };
      };
    };
    
    // console.log(convertedCategories);
    // console.log(convertedData);

    let series = []
    for (let i = 0; i < 6; i++) {
      series.push({name:`Pump ${i+1}`,data:convertedData[i]})
      
      // for (const element of convertedCategories) {
        
      // }

    }

    drawLineChart2(convertedCategories,series,'.js-chart-pump-history','Time','Pumps','Pump Usage History');

  };
};



const drawLineChart = function(categories,data,chartSelector,chartNameX,chartNameY,chartName,min,max) {
  var options = {
    series: [{
    name: chartName,
    data: data
  }],
    chart: {
    type: 'area',
    stacked: false,
    height: 350,
    zoom: {
      type: 'x',
      enabled: true,
      autoScaleYaxis: true
    },
    toolbar: {
      autoSelected: 'zoom'
    }
  },
  dataLabels: {
    enabled: false
  },
  markers: {
    size: 0,
  },
  title: {
    text: chartNameY,
    align: 'left'
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.5,
      opacityTo: 0,
      stops: [0, 90, 100]
    },
  },
  yaxis: {
    title: {
      text: chartNameY
    },
    min: min,
    max: max
  },
  xaxis: {
    categories: categories,
    title: {
      text: chartNameX
    }
  },
  tooltip: {
    shared: false,
    y: {
      formatter: function (val) {
        return (val / 1000000).toFixed(0)
      }
    }
  },
  colors: ['#748C00'],
  };

  var chart = new ApexCharts(document.querySelector(chartSelector), options);
  chart.render();
}



const drawLineChart2 = function(categories,data,chartSelector,chartNameX,chartNameY,chartName,min,max,sign="ml") {
  console.log(data)
  console.log(categories)
  console.log(chartName)

  var options = {
    series: data,
    chart: {
    height: 350,
    type: 'line',
    dropShadow: {
      enabled: true,
      color: '#000',
      top: 18,
      left: 7,
      blur: 10,
      opacity: 0.2
    },
    toolbar: {
      show: false
    }
  },
  colors: ['#748C00','#008C79','#00178C','#67008C','#8C0000','#C5C51F'],
  dataLabels: {
    enabled: true,
  },
  stroke: {
    curve: 'smooth'
  },
  title: {
    text: chartName,
    align: 'center'
  },
  grid: {
    borderColor: '#e7e7e7',
    row: {
      colors: ['#f3f3f3', 'transparent'],
      opacity: 0.5
    },
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val + sign; 
    }
  },
  markers: {
    size: 1
  },
  xaxis: {
    categories: categories,
    title: {
      text: chartNameX
    }
  },
  yaxis: {
    title: {
      text: chartNameY
    },
    min: 0,
    max: 250
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    floating: true,
    offsetY: -25,
    offsetX: -5
  }
  };

  var chart = new ApexCharts(document.querySelector(chartSelector), options);
  chart.render();
}


const drawBarChart = function(categories,data,chartSelector,chartName,sign) {
  // console.log(chartName)
  var options = {
    series: [{
    name: chartName,
    data: data
  }],
    chart: {
    height: 350,
    type: 'bar',
    fill: '#000'
  },
  plotOptions: {
    bar: {
      borderRadius: 10,
      dataLabels: {
        position: 'top', // top, center, bottom
      },
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val + sign; 
    },
    offsetY: -20,
    style: {
      fontSize: '12px',
      colors: ["black"]
    }
  },
  
  xaxis: {
    categories: categories,
    position: 'bottom',
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#E6F3A3',
          colorTo: '#748C00',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    }
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
      formatter: function (val) {
        return val + sign;
      }
    }
  
  },
  title: {
    text: chartName,
    floating: true,
    offsetY: 0,
    align: 'center',
    style: {
      color: '#444'
    }
  } ,
  fill: {
    colors: ['#748C00']
  }
  };

  chart = new ApexCharts(document.querySelector(chartSelector),options)
  chart.render()
}



// Socket listening

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("Connection established.");
  });

  let url = window.location.pathname.split('/');
  // console.log(url);  
  if ((url[1] == "Menu.html") | (url[4] == "Menu.html")) {
    console.log("Welcome to the Menu Page.");
    page = "Menu.html"
    
  } 
  
  if ((url[1] == "Stats.html") | (url[4] == "Stats.html")) {
    console.log("Welcome to the Analytics Page");
    page = "Stats.html"
  }

  socket.emit('F2B_request_data',{'url':page});
  listenToSocketMenu();
  listenToSocketStat();
};


const listenToSocketMenu = function() {
  socket.on("B2F_cocktail_menu", function (jsonObject) {
    console.log("Received cocktail list");
    console.log(jsonObject);
    addCocktails(jsonObject);
  });
};

const listenToSocketStat = function() {
  socket.on("B2F_current_temperature", function (temperature) {
    console.log("Received current temperature");
    // console.log(jsonObject);
    showCurrentTemperature(temperature);
  });

  socket.on("B2F_cocktail_popularity", function (jsonObject) {
    console.log("Received cocktail popularity");
    // console.log(jsonObject);
    showCocktailPopularity(jsonObject);    
  });


  socket.on("B2F_sensor_history", function (jsonObject) {
    console.log("Received sensor history")
    // console.log(jsonObject);
    showHistorySensors(jsonObject);
  });


  //   socket.on("B2F_cocktail_history", function (jsonObject) {
  //     console.log("Received cocktail history");
  //     // console.log(jsonObject);
  //     showHistoryCocktail(jsonObject);    
  // });

  // socket.on("B2F_current_volume", function (jsonObject) {
  //   // console.log("Received latest history");
  //   // console.log(jsonObject);
  //   showCurrentVolume(jsonObject);
  // });

  socket.on("B2F_actuator_history", function (jsonObject) {
    console.log("Received actuator list");
    showHistoryActuator(jsonObject);
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToSocket();
  document.querySelector(".js-shutdown").addEventListener('click',function() {socket.emit("F2B_shutdown")});
});
