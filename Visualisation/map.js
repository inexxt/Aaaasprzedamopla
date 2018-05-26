var fullPage = {x: innerWidth, y: innerHeight};
var mid = {x: fullPage.x/2, y: fullPage.y/2};
var mapSize = {x: 1280, y: 812};
var mapStart = {x: mid.x - (mapSize.x/2), y: mid.y - (mapSize.y/2)};
var percSize = 0.8;
var percText = 0.1;
var percStartYtext = (mapSize.y/8)*(1 + percSize);

var Percents = {dead: 10, sick: 30, healthy: 50, safe: 10};
var t = 20;

var nof_points = 50;


var canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d");

canvas.width = fullPage.x;
canvas.height = fullPage.y;


// var background = new Image();
// background.src = "mapa_poznania.jpg";
//
// background.onload = function(){
//     ctx.drawImage(background,mapStart.x,mapStart.y);
// }

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

ctx.font = "30px Comic Sans MS";
ctx.fillStyle = "red";
ctx.textAlign = "center";

var i;
for (i = 0; i < 4; i++){
  ctx.fillText(textLabels[i].name, textLabels[i].x, percStartYtext);
}

var locs = [[[mid.x+150, mid.y+150], [mid.x, mid.y]]];

const numPoints = 1;
const points = d3.range(numPoints).map(index => ({
  id: index,
  color: "red",
  x: locs[index][0][0],
  y: locs[index][0][1],
  iter: 0
}));

// function gridLayout(points, pointWidth, j) {
//   const pointHeight = pointWidth;
//
//   points.forEach((point, i) => {
//     point.x = locs[i][j][0];
//     point.y = locs[i][j][1];
//   });
//   return points;
// }

function draw() {
  for (let i = 0; i < points.length; i++) {
    const point = points[i];
    ctx.fillStyle = point.color;
    ctx.fillRect(point.x, point.y, pointWidth, pointWidth);
  }

  ctx.restore();
}

const pointWidth = 50;
N = 2;
let k;
for (k = 0; k < N; k++){
  draw();
  points.forEach((point, i) => {
    point.x = locs[i][k][0];
    point.y = locs[i][k][1];
  });
};

draw()



// draw();
//
// gridLayout(points, pointWidth);
//
//   // update what is drawn on screen
// draw();

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
