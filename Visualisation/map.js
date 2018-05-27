var fullPage = {x: innerWidth, y: innerHeight};
var mid = {x: fullPage.x/2, y: fullPage.y/2};
var mapSize = {x: 1280, y: 812};
var mapStart = {x: mid.x - (mapSize.x/2), y: mid.y - (mapSize.y/2)};
var percSize = 0.8;
var percText = 0.1;
var percStartYtext = (mapSize.y/8)*(1 + percSize);

var Percents = [10, 30, 50];

var nof_points = 50;

var low_canvas = document.getElementById("low_canvas"),
    low_ctx = low_canvas.getContext("2d");

var percPos = {
  dead:  mapStart.x + mapSize.x/8,
  sick: mapStart.x + mapSize.x*(3/8),
  healthy: mapStart.x + mapSize.x*(5/8),
  safe: mapStart.x + mapSize.x*(7/8)};


var textLabels = [
  {name: "Dead", x: percPos.dead},
  {name: "Sick", x: percPos.sick},
  {name: "Healthy", x: percPos.healthy},
  {name: "Safe", x: percPos.safe}];

low_canvas.width = fullPage.x;
low_canvas.height = fullPage.y;

var background = new Image();
background.src = "mapa_poznania.jpg";

background.onload = function(){
 low_ctx.drawImage(background,mapStart.x,mapStart.y);
 var i;
 for (i = 0; i < 4; i++){
    low_ctx.fillText(textLabels[i].name, textLabels[i].x, percStartYtext);
  }
}

var canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d");

canvas.width = fullPage.x;
canvas.height = fullPage.y;




low_ctx.font = "30px Comic Sans MS";
low_ctx.fillStyle = "red";
low_ctx.textAlign = "center";

pointWidth = 4;

function draw() {
  ctx.clearRect(0, 0, width, height);
  for (let i = 0; i < humans.length; i++) {
    const human = humans[i];
    ctx.fillStyle = "green";
    ctx.fillRect(human[0], human[1], pointWidth, pointWidth);
  }
  ctx.restore();
}

function add_points(agents, color){
  for (let j = 0; j < agents.length; j++) {
    const agent = agents[j];
    ctx.fillStyle = color;
    ctx.fillRect(agent[0], agent[1], pointWidth, pointWidth);
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function funkcja() {
  for (let i = 0; i < locs.length; i++){
      var humans = locs[i][0];
      var zombies = locs[i][1];
      ctx.clearRect(0, 0, mapSize.x, mapSize.y);
      add_points(zombies, "red")
      add_points(humans, "lightblue")
      ctx.restore();
      await sleep(50);
  }

}



funkcja()

// var percents = svg.selectAll("text")
//                            .data(percents)
//                            .enter()
//                            .append("text")
//                            .attr({
//                              "x": function(d) {return d.x;},
//                              "y": percStartYtext,
//                              "font-family": "sans-serif",
//                              "fill": "red",
//                              "text-anchor": "middle"})
//                            .text(function(d) {return d.name;});
