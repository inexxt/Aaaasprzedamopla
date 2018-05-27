var zoom = 3

var fullPage = {x: innerWidth*zoom, y: innerHeight*zoom};
var mid = {x: fullPage.x/2, y: fullPage.y/2};

var mapSize = {
    x: data["_10"][0] - data["_00"][0],
    y: data["_01"][1] - data["_00"][1]}

var part = fullPage.y/mapSize.y

mapSize = {x: mapSize.x*part, y: mapSize.y*part}

var mapStart = {x: mid.x - (mapSize.x/2), y: mid.y - (mapSize.y/2)};
var percSize = 0.8;
var percText = 0.1;
var percStartYtext = (mapSize.y/8)*(1 + percSize);

function generate_points(p_list){
    var s = "";
    for (point of p_list){
        s += "" + point[0]*part.toString() + " " + (fullPage.y - point[1]*part).toString() + ", ";
        };
    return s.slice(0,-1)
    };

//var low_canvas = document.getElementById("low_canvas"),
//    low_ctx = low_canvas.getContext("2d");
var low_canvas = d3.select("body")
   .append("svg")
   .attr("height", fullPage.y)
   .attr("width", fullPage.x);

low_canvas.append("polygon")
   .attr("points", generate_points(data["boundary"]))
   .style("fill", "green")
   .style("stroke", "black")
   .style("strokeWidth", "10px");

for (building of buildings["buildings"]){
    low_canvas.append("polygon")
       .attr("points", generate_points(building))
       .style("fill", "blue")
       .style("stroke", "black")
       .style("strokeWidth", "1px");
    }


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

var canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d");

canvas.width = fullPage.x;
canvas.height = fullPage.y;




//low_canvas.font = "30px Comic Sans MS";
//low_canvas.fillStyle = "red";
//low_canvas.textAlign = "center";

pointWidth = 10*zoom;




function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
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
    ctx.fillRect(agent[0]*part, agent[1]*part, pointWidth, pointWidth);
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function plot_points() {
  for (let i = 0; i < locs.length; i++){
      var humans = locs[i][0];
      console.log(humans)
      var zombies = locs[i][1];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      add_points(zombies, "red")
      add_points(humans, "lightblue")
      ctx.restore();
      await sleep(10);
  }

}


plot_points()

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
